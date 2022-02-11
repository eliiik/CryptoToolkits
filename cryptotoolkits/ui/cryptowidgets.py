from lib2to3.pgen2 import token
import ipywidgets as widgets

def create_slider(name, in_value, in_min, in_max, in_step, in_format):
    return widgets.FloatSlider(
            value=in_value,
            min=in_min,
            max=in_max,
            step=in_step,
            description=name+": ",
            disabled=False,
            continuous_update=True,
            orientation='horizontal',
            readout=True,
            readout_format=in_format,
        )

def create_range_slider(name, in_value, in_min, in_max):
    return create_slider(name, in_value, in_min, in_max, 0.01, ".2f")

def create_token_slider(token_name, token_default_price=10, token_max_price=100):
    return create_range_slider(token_name, token_default_price, 0, token_max_price)

def create_01_float_slider(name, in_value):
    return create_range_slider(name, in_value, 0, 1)

class Token(object):
    def __init__(self, token_name, token_price) -> None:
        self._token_name = token_name
        self._token_price = token_price

    @property
    def token(self):
        return self._token_name

    @property
    def price(self):
        return self._token_price

class BorrowToken(Token):
    def __init__(self, token_name, token_amount=0,
                                   token_default_price=10, 
                                   token_max_price=100, 
                                   borrow_apr=-0.06) -> None:
        super().__init__(token_name, token_default_price)
        self._amount = token_amount
        self._token_max_price = token_max_price
        self._borrow_apr = borrow_apr
        self.token_widget = None
        self.view = None
        self.ui_widgets = {}
        self.create_view()

    def create_view(self):
        self.token_widget = create_token_slider(self.token, self.price, self._token_max_price)
        self.token_amount_widget = create_range_slider("Amount", self._amount, 0, 100000)
        self.token_borrow_apr = create_slider("Borrow APR", self._borrow_apr, -0.2, 0.4, 0.001, ".3f")
        token_view = widgets.HBox([self.token_widget, self.token_amount_widget])
        self.view = widgets.VBox([token_view, self.token_borrow_apr])
        self.ui_widgets["b"+self.token+"_price"] = self.token_widget
        self.ui_widgets["b"+self.token+"_amount"] = self.token_amount_widget
        self.ui_widgets["b"+self.token+"_apr"] = self.token_borrow_apr

class SupplyToken(Token):
    def __init__(self, token_name, token_amount=0,
                                   token_default_price=10, 
                                   token_max_price=100, 
                                   token_collat_factor=0.7, 
                                   token_liquid_factor=0.8, 
                                   supply_apr=0.07) -> None:
        super().__init__(token_name, token_default_price)
        self._amount = token_amount
        self._token_max_price = token_max_price
        self._token_collat_factor = token_collat_factor
        self._token_liquid_factor = token_liquid_factor
        self._supply_apr = supply_apr
        self.token_widget = None
        self.view = None
        self.ui_widgets = {}
        self.create_view()

    def create_view(self):
        self.token_widget = create_token_slider(self.token, self.price, self._token_max_price)
        self.token_amount_widget = create_range_slider("Amount", self._amount, 0, 100000)
        self.token_collat_widget = create_01_float_slider("Col. Factor", self._token_collat_factor)
        self.token_liquid_widget = create_01_float_slider("Liquid Factor", self._token_liquid_factor)
        self.token_supply_apr = create_slider("Supply APR", self._supply_apr, 0, 0.4, 0.001, ".3f")
        token_view = widgets.HBox([self.token_widget, self.token_amount_widget])
        factor_view = widgets.HBox([self.token_collat_widget, self.token_liquid_widget])
        self.view = widgets.VBox([token_view, factor_view, self.token_supply_apr])
        self.ui_widgets["s"+self.token+"_price"] = self.token_widget
        self.ui_widgets["s"+self.token+"_amount"] = self.token_amount_widget
        self.ui_widgets["s"+self.token+"_collat"] = self.token_collat_widget
        self.ui_widgets["s"+self.token+"_liquid"] = self.token_liquid_widget
        self.ui_widgets["s"+self.token+"_apr"] = self.token_supply_apr

def create_token_accordion(tokens, title):
    views = [i.view for i in tokens]
    w = widgets.VBox(views)
    return widgets.Accordion([w], titles=[title])
