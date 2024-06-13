import panel as pn
import xarray as xr
import holoviews as hv
from holoviews import opts
import hvplot.xarray

hv.extension("bokeh")

## Load data

rda_url = 'https://data.rda.ucar.edu/'
annual_means = rda_url + 'pythia_era5_24/annual_means/'
xrds = xr.open_dataset(annual_means + "temp_2m_annual_1940_2023.zarr", engine= 'zarr')
xrds.load()

xrds['VAR_2T_ANOM_FROM_1940'] = xrds['VAR_2T'] - xrds['VAR_2T'][0]

## Widget configuration
w_time = pn.widgets.IntSlider(name='Year', start=0, end=83)

w_var = pn.widgets.Select(name='Data Variable', options=list(xrds.data_vars))

dataset_controls = pn.WidgetBox(
                                '## Dataset Controls', 
                                w_var, 
                                )

w_cmap = pn.widgets.Select(name='Colormap', options=['inferno', 'plasma', 'coolwarm'])

w_plot_type = pn.widgets.Select(name='Plot Type', options=['Color Plot', 'Contour', 'Filled Contour'])

plot_controls = pn.WidgetBox(
                            '## Plot Controls',
                            w_plot_type,
                            w_cmap, 
                            )

w_player = pn.widgets.Player(
    value=0,
    start=0,
    end=83,
    name="Year",
    loop_policy="loop",
    interval=300,
    align="center",
    width_policy='fit'
)

## Function to create the plot

def plot_ds(time, var, cmap, plot_type):
    clim = (xrds[var].values.min(), xrds[var].values.max())
    
    if plot_type == "Color Plot":
        return xrds[var].isel(time=time).hvplot(cmap=cmap, 
                                                              title=str(f"{var} year {time}"),
                                                              clim=clim,
                                                              dynamic=False,
                                                              rasterize=True,
                                                              precompute=True,
                                               ).opts(framewise=False)
    
    elif plot_type == "Contour":
        return xrds[var].isel(time=time).hvplot.contour(cmap=cmap,
                                          dynamic=False,
                                          rasterize=True,
                                          title=str(f"{var} Year: {time}"),
                                          clim=clim,
                                          precompute=True,).opts(framewise=False)
    elif plot_type == "Filled Contour":
        return xrds[var].isel(time=time).hvplot.contourf(cmap=cmap,
                                          dynamic=False,
                                          rasterize=True,
                                          title=str(f"{var} Year: {time}"),
                                          clim=(200, 300),
                                          precompute=True,).opts(framewise=False)     

## Panel App configuration

controls = pn.Column(dataset_controls, plot_controls)

app = pn.Row(
    controls,
    pn.Column(pn.panel(
        hv.DynamicMap(pn.bind(
            plot_ds, 
            time=w_player,
            var=w_var,
            cmap=w_cmap,
            plot_type = w_plot_type
        )
                     )
    ),
             w_player)
).servable()