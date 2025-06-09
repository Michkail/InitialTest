from decimal import Decimal


class MatchingEngine:
    def match_orders(self, buy_orders, sell_orders):
        matched = []

        for buy in buy_orders:
            for sell in sell_orders:
                if buy["asset"] == sell["asset"] and buy["amount"] <= sell["amount"]:
                    matched.append((buy, sell))
                    break
                
        return matched
