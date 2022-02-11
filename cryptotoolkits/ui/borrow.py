
from ipywidgets import interact, interactive, fixed, interact_manual
import ipywidgets as widgets
from IPython.display import display
from . import cryptowidgets
from importlib import reload
reload(cryptowidgets)

class BorrowLendingAnalyze(object):
    def __init__(self, supplies, borrows, use_col=False):
        self._supplies = supplies
        self._borrows = borrows
        self._use_col = use_col

    def show(self):
        supply_list = [cryptowidgets.SupplyToken(i["token"], i["amount"], 
                                              i["current_price"], i["max_price"], 
                                              i["colat_price"], i["liquid_price"],
                                              i["apr"]) for i in self._supplies]
        supply_accordion = cryptowidgets.create_token_accordion(supply_list, "Supplied")
        display(supply_accordion)    

        borrow_list = [cryptowidgets.BorrowToken(i["token"], i["amount"], 
                                              i["current_price"], i["max_price"],
                                              i["apr"]) for i in self._borrows]  

        borrow_accordion = cryptowidgets.create_token_accordion(borrow_list, "Borrowed")

        display(borrow_accordion)

        for i in supply_list:
            for j in borrow_list:
                if i.token == j.token:
                    widgets.jslink((i.token_widget, "value"), (j.token_widget, "value"))
                    break
        
        widgets_dict = dict()
        for i in supply_list+borrow_list:
            widgets_dict.update(i.ui_widgets)

        # calc totol deposite value
        health_rate = 1
        limit_used = 0
        total_apr = 0

        hr_w = widgets.Text(
            value='{:.2f}'.format(health_rate),
            placeholder='1.00',
            description='健康系数：',
            disabled=False
        )

        lim_w = widgets.Text(
            value='{:.2f}'.format(limit_used),
            placeholder='1.00',
            description='Limit Used: ',
            disabled=False
        )

        apr_val = widgets.Text(
            value='{:.2f}'.format(total_apr),
            placeholder='1.00',
            description='每月利息：',
            disabled=False
        )

        def f(**widgets_dict):
            cols_value = 0
            liq_value = 0
            supply_interest = 0
            for i in supply_list:
                token_value = i.token_widget.value * i.token_amount_widget.value
                cols_value += token_value * i.token_collat_widget.value
                liq_value += token_value * i.token_liquid_widget.value
                supply_interest += token_value * i.token_supply_apr.value
            
            brows_value = 0
            borrow_interst = 0
            for j in borrow_list:
                brows_value += j.token_widget.value * j.token_amount_widget.value
                borrow_interst += brows_value * j.token_borrow_apr.value
            
            _health_rate = (cols_value if self._use_col else liq_value) / brows_value 
            _total_apr = (supply_interest + borrow_interst) / 12
            hr_w.value =  "{:.2f}".format(_health_rate)
            lim_w.value = "{:.2f}".format(brows_value/(cols_value if self._use_col else liq_value))
            apr_val.value = "{:.2f}".format(_total_apr)

        out = widgets.interactive_output(f, widgets_dict)

        display(hr_w, lim_w, apr_val, out)

