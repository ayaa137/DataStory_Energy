# ------------------------------------------------------------------
# Build a country-year panel combining:
#   - World Bank WDI indicators (education, labor, macro, trade, governance)
#   - WHO Global Health Observatory obesity data (BMI proxy)
#
# WDI no longer serves the obesity/overweight family (SH.STA.OB18.ZS etc.)
# in its live database, so that piece is pulled directly from WHO GHO
# and merged in by country code ISO3 and year.
# ------------------------------------------------------------------

# install.packages(c("WDI", "httr2", "jsonlite"))
library(tidyverse)
library(WDI)
library(httr2)
library(jsonlite)

# --------------------------------------------------------------
# 1. World Bank WDI indicators
# --------------------------------------------------------------

wdi_indicators <- c(
  total_population = "SP.POP.TOTL",
  gdp_total_usd = "NY.GDP.MKTP.CD",
  gdp_per_capita_usd = "NY.GDP.PCAP.CD",
  secondary_enrollment_gross_pct = "SE.SEC.ENRR",
  unemployment_rate_pct = "SL.UEM.TOTL.ZS",
  inflation_cpi_pct = "FP.CPI.TOTL.ZG",
  life_expectancy_years = "SP.DYN.LE00.IN",
  fuel_exports_pct_merch_exports = "TX.VAL.FUEL.ZS.UN",
  fuel_imports_pct_merch_imports = "TM.VAL.FUEL.ZS.UN",
  voice_accountability_index = "GOV_WGI_VA.EST"
)

wdi_raw <- WDI(
  indicator = wdi_indicators,
  country = "all",
  start = 1960,
  end = 2025,
  extra = TRUE
)
wdi <- wdi_data |>
  as_tibble() |>
  select(-lastupdated) |>
  summarise(
    across(everything(), ~ first(na.omit(.))),
    .by = c(country, year)
  ) |>
  filter(region != "Aggregates") |>
  select(
    country_name = country,
    country_code = iso3c,
    year,
    region,
    income_group = income,
    all_of(names(wdi_indicators))
  ) |>
  arrange(country_name, year)

# --------------------------------------------------------------
# 2. WHO GHO obesity data (BMI proxy)
#    NCD_BMI_30C = Prevalence of obesity, adults 18+, BMI >= 30 (crude estimate, %)
#    Dim1 filter keeps only "both sexes" rows (drops M/F breakdowns)
# --------------------------------------------------------------

gho_resp <- request("https://ghoapi.azureedge.net/api/NCD_BMI_30C") |>
  req_perform() |>
  resp_body_json(simplifyVector = TRUE)

bmi_data <- gho_resp$value |>
  as_tibble() |>
  filter(Dim1 == "SEX_BTSX", SpatialDimType == "COUNTRY") |>
  transmute(
    country_code = SpatialDim,
    year = as.integer(TimeDim),
    obesity_prevalence_pct = NumericValue
  ) |>
  distinct(country_code, year, .keep_all = TRUE) |>
  arrange(country_code, year)

# --------------------------------------------------------------
# 3. Merge into one panel and save
# --------------------------------------------------------------

indicator_cols <- c(names(wdi_indicators), "obesity_prevalence_pct")

panel <- wdi |>
  left_join(bmi_data, by = c("country_code", "year")) |>
  arrange(country_name, year) |>
  group_by(country_code) |>
  fill(all_of(indicator_cols), .direction = "down") |>
  ungroup()

write_csv(panel, "data/country_panel_wdi_who.csv")
