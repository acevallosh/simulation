from typing import Optional
from decimal import Decimal as Dec
import random

import orderbook as ob
from managers import HavvenManager as hm
from .marketplayer import MarketPlayer


class Banker(MarketPlayer):
    """Wants to buy havvens and issue nomins, in order to accrue fees."""

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.fiat_havven_order: Optional["ob.Bid"] = None
        self.nomin_havven_order: Optional["ob.Bid"] = None
        self.rate: Dec = hm.round_decimal(Dec(random.random() * 0.05))

    def step(self) -> None:
        if hm.round_decimal(self.available_fiat) > 0:
            if self.fiat_havven_order:
                self.fiat_havven_order.cancel()
            self.fiat_havven_order = self.sell_fiat_for_havvens_with_fee(hm.round_decimal(self.available_fiat * self.rate))

        if hm.round_decimal(self.available_nomins) > 0:
            if self.nomin_havven_order:
                self.nomin_havven_order.cancel()
            self.nomin_havven_order = self.sell_nomins_for_havvens_with_fee(self.available_nomins)

        if hm.round_decimal(self.available_havvens) > 0:
            self.escrow_havvens(self.available_havvens)

        issuable = self.max_issuance_rights() - self.issued_nomins
        if hm.round_decimal(issuable) > 0:
            self.issue_nomins(issuable)