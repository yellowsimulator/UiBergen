from rpy2.robjects.lib import ggplot2

p = ggplot2.ggplot(faithful_data) + \
    ggplot2.aes_string(x = "eruptions") + \
    ggplot2.geom_histogram(fill = "lightblue") + \
    ggplot2.geom_density(ggplot2.aes_string(y = '..count..'), colour = "orange") + \
    ggplot2.geom_rug() + \
    ggplot2.scale_x_continuous("Eruption duration (seconds)") + \
    ggplot2.opts(title = "Old Faithful eruptions")

p.plot()
