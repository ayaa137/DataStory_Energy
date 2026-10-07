# Define Color and read temperature data

warming_stripe_colors <- c(
  "#08306b",
  "#08519c",
  "#2171b5",
  "#4292c6",
  "#6baed6",
  "#9ecae1",
  "#c6dbef",
  "#deebf7",
  "#FFFFFF",
  "#fee0d2",
  "#fcbba1",
  "#fc9272",
  "#fb6a4a",
  "#ef3b2c",
  "#cb181d",
  "#a50f15",
  "#67000d"
)
temperature <- read_csv(
  "data/HadCRUT.5.0.2.0.analysis.summary_series.global.annual.csv"
)


# Warming stripe plot

temperature |>
  ggplot(aes(x = Time, y = 1, fill = `Anomaly (deg C)`)) +
  geom_tile() +
  scale_fill_gradientn(
    colors = warming_stripe_colors,
    rescaler = ~ scales::rescale_mid(.x, mid = 0)
  ) +
  # The rescale put the mid-point to zero
  theme_void() #+
theme(legend.position = "none")

# As a points and line plot

temperature |>
  ggplot(aes(x = Time, y = `Anomaly (deg C)`, fill = `Anomaly (deg C)`)) +
  geom_line() +
  geom_point(size = 5, shape = "circle filled") + # Example of filled shapes!
  scale_fill_gradientn(
    colors = warming_stripe_colors,
    rescaler = ~ scales::rescale_mid(.x, mid = 0)
  ) +
  theme_minimal() +
  theme(legend.position = "none")
