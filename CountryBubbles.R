# Variable Names in country_panel_wdi_who.csv
#
# See Details on corresponding lecture slides
#
# country_name / country_code / year
# region (categorical)
# income_group (categorical)
# total_population — SP.POP.TOTL
# gdp_total_usd — NY.GDP.MKTP.CD
# gdp_per_capita_usd — NY.GDP.PCAP.CD
# life_expectancy_years — SP.DYN.LE00.IN
# secondary_enrollment_gross_pct — SE.SEC.ENRR
# unemployment_rate_pct — SL.UEM.TOTL.ZS
# inflation_cpi_pct — FP.CPI.TOTL.ZG
# fuel_exports_pct_merch_exports — TX.VAL.FUEL.ZS.UN
# fuel_imports_pct_merch_imports — TM.VAL.FUEL.ZS.UN
# voice_accountability_index — GOV_WGI_VA.EST
# obesity_prevalence_pct — NCD_BMI_30C (WHO GHO)
#
# See data compilation script in data/ with download using WDI and WHO APIs (wrapped in R packages)
# With research on WDI indicators, you can extend the dataset

# Package and Data
library(tidyverse)
library(ggbeeswarm)
library(ggridges)
df <- read_csv("data/country_panel_wdi_who.csv")

# Hans Rosling's Version (with different regions)
## Without much styling of label
df |>
  filter(year == 2018) |>
  ggplot(aes(
    x = gdp_per_capita_usd,
    y = life_expectancy_years,
    size = total_population,
    color = region
  )) +
  geom_point(alpha = 0.8) +
  scale_x_log10() +
  scale_size_area(max_size = 15) +
  theme_minimal()

# Paulsen's version
## Without much styling of labels
df |>
  filter(year == 2018) |>
  ggplot(aes(
    x = life_expectancy_years,
    y = gdp_per_capita_usd,
    size = total_population,
    color = region
  )) +
  geom_point(alpha = 0.8) +
  scale_size_area(max_size = 15) +
  theme_minimal()

# Bubble Plots Facetted by years
## With some styling specs
df |>
  filter(year %in% c(1988, 1998, 2018)) |>
  ggplot(aes(
    x = gdp_per_capita_usd,
    y = life_expectancy_years,
    size = total_population,
    color = region
  )) +
  geom_point(alpha = 0.8) +
  scale_x_log10(breaks = c(300, 3000, 30000)) +
  scale_y_continuous(limits = c(40, 87)) +
  scale_size_area(max_size = 15) +
  facet_wrap(~year) +
  labs(x = "GDP per capita (USD)", y = "Life expectancy (years)") +
  theme_minimal() +
  theme(legend.position = "bottom", panel.border = element_rect()) +
  guides(
    size = "none",
    color = guide_legend(ncol = 4, override.aes = list(size = 4), title = NULL)
  )


# Density ridge plots
## Consider: Uses weight to weight by population in the density plot.
## What is the difference if we do not weight by population, technically and in interpretation
df |>
  filter(year == 2018) |>
  ggplot(aes(
    x = life_expectancy_years,
    y = region,
    weight = total_population,
    fill = region
  )) +
  geom_density_ridges()


# Ranking Plot
## Filtered fro large countries to allow readability of the list of country names
df |>
  filter(year == 2016, total_population > 20000000) |>
  summarize(
    mean_var = mean(life_expectancy_years),
    .by = c(country_name, region)
  ) |>
  arrange(mean_var) |>
  ggplot(aes(
    x = mean_var,
    y = country_name |> fct_inorder(),
    fill = region
  )) +
  geom_col() +
  labs(
    title = "Life Expectancy, Countries with more than 20 Mio.",
    x = "",
    y = ""
  ) +
  scale_fill_brewer(palette = "Dark2") +
  theme_minimal()

# --------------------------------------------------------------
# YOUR AREA FOR YOU GREAT BUBBLE AND OTHER COUNTRY PLOT
# --------------------------------------------------------------
