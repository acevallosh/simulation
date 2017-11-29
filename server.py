"""server.py: Functions for setting up the simulation/visualisation server."""

from typing import List

from visualization.modules import ChartModule, OrderBookModule, WealthModule, PortfolioModule, \
    CurrentOrderModule, CandleStickModule, PastOrdersModule

from visualization.UserParam import UserSettableParameter
from visualization.ModularVisualization import ModularServer
from visualization.VisualizationElement import VisualizationElement

import model


def make_server(n_agents: int = 50, ur: float = 0.3,
                cont_orders: bool = True, threaded=True) -> ModularServer:
    """
    Set up the simulation/visualisation server and return it.

    "Label": "0"/"1" is a workaround to show the graph label where there is only one label
      (the graphs with only one label wont show the label value, and also show multiple
      values at the same time)
    """
    ref_colour = "lightgrey"

    charts: List[VisualizationElement] = [
        CandleStickModule([
            {"Label": "NominFiatPriceData", "orderbook": "NominFiatOrderBook",
             "AvgColor": "rgba(0,191,255,0.6)", "VolumeColor": "rgba(0,191,255,0.3)"}  # deepskyblue
        ]),

        CandleStickModule([
            {"Label": "HavvenFiatPriceData", "orderbook": "HavvenFiatOrderBook",
             "AvgColor": "rgba(255,0,0,0.6)", "VolumeColor": "rgba(255,0,0,0.3)"}  # red
        ]),

        CandleStickModule([
            {"Label": "HavvenNominPriceData", "orderbook": "HavvenNominOrderBook",
             "AvgColor": "rgba(153,50,204,0.6)", "VolumeColor": "rgba(153,50,204,0.3)"}  # darkorchid
        ]),

        # ChartModule([
        #     {"Label": "Max Wealth", "Color": "purple"},
        #     {"Label": "Min Wealth", "Color": "orange"},
        # ]),

        PortfolioModule([{"Label": "WealthBreakdown"}], fiat_values=False),

        WealthModule([{"Label": "Wealth"}]),

        ChartModule([
            {"Label": "Avg Profit %", "Color": "grey"},
            {"Label": "Bank Profit %", "Color": "blue"},
            {"Label": "Arb Profit %", "Color": "red"},
            {"Label": "Rand Profit %", "Color": "green"},
            {"Label": "NomShort Profit %", "Color": "orchid"},
            {"Label": "EscrowNomShort Profit %", "Color": "darkorchid"},
            {"Label": "0", "Color": ref_colour}
        ]),

        CurrentOrderModule([{"Label": "PlayerBidAskVolume"}]),

        PastOrdersModule([{"Label": "TotalMarketVolume"}]),

        ChartModule([
            {"Label": "Havven Demand", "Color": "red"},
            {"Label": "Havven Supply", "Color": "orange"},
        ]),

        ChartModule([
            {"Label": "Nomin Demand", "Color": "deepskyblue"},
            {"Label": "Nomin Supply", "Color": "purple"},
        ]),

        ChartModule([
            {"Label": "Fiat Demand", "Color": "darkgreen"},
            {"Label": "Fiat Supply", "Color": "lightgreen"},
        ]),

        ChartModule([
            {"Label": "Nomins", "Color": "deepskyblue"},
            {"Label": "Escrowed Havvens", "Color": "darkred"},
        ]),

        ChartModule([
            {"Label": "Fee Pool", "Color": "blue"},
            {"Label": "0", "Color": ref_colour}
        ]),

        ChartModule([
            {"Label": "Fees Distributed", "Color": "blue"},
            {"Label": "0", "Color": ref_colour}
        ]),

        ChartModule([
            {"Label": "Havven Nomins", "Color": "deepskyblue"},
            {"Label": "Havven Havvens", "Color": "red"},
            {"Label": "Havven Fiat", "Color": "darkgreen"},
        ]),

        ChartModule([
            {"Label": "Gini", "Color": "navy"},
            {"Label": "0", "Color": ref_colour}
        ]),

        OrderBookModule([{"Label": "NominFiatOrderBook"}]),

        OrderBookModule([{"Label": "HavvenFiatOrderBook"}]),

        OrderBookModule([{"Label": "HavvenNominOrderBook"}])
    ]

    n_slider = UserSettableParameter(
        'slider', "Number of agents", n_agents, 20, 175, 1
    )

    ur_slider = UserSettableParameter(
        'slider', "Utilisation Ratio", ur, 0.0, 1.0, 0.01
    )

    match_checkbox = UserSettableParameter(
        'checkbox', "Continuous order matching", cont_orders
    )

    # the none value will randomize the data on every model reset
    agent_fraction_selector = UserSettableParameter(
        'agent_fractions', "Agent fraction selector", None
    )

    server = ModularServer(threaded, model.HavvenModel, charts, "Havven Model (Alpha)",
                           {"num_agents": n_slider, "utilisation_ratio_max": ur_slider,
                            "match_on_order": match_checkbox, 'agent_fractions': agent_fraction_selector})
    return server
