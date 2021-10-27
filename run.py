from time import sleep
from coinbase.wallet.client import Client
from coinbase.wallet.error import AuthenticationError
from data import currency_code, percentage_change, api_key, api_secret

client= Client(api_key,api_secret)

total= 0
message = []

try:
    accounts= client.get_accounts()
    for wallet in accounts.data:
        message.append(str(wallet['name'])+ ' ' + str(wallet['native_balance']))
        value = str(wallet['native_balance']).replace(currency_code, '')
        total += float(value)
    message.append('Totale Bilancio: ' + currency_code + ' ' + str(total))
    print('\n'.join(message))

    #Take user input
    user_limit_order = float(input("Enter a price for your Bitcoin limit order (" + currency_code + "): "))
    user_amount_spent = float(input("Enter how much you want to spend (" + currency_code + "): "))

    #Creating the loop
    
    start_price = client.get_spot_price(currency=currency_code)

    while(True):
        #Reset currents and find percentage change
        buy_price = client.get_buy_price(currency=currency_code)
        percentage_gainloss = percentage_change(start_price.amount, buy_price.amount)
        
        #print bitcoin curent price, and percentage chage
        print('Bitcoin is ' + str(buy_price.amount) + '\nPercent change in last 60 seconds: ' + format(percentage_gainloss, ".3f") + '%')
        
        #if float(sell_price.amount) <= sell_price_threshold:
        ##sell = account.sell(amount='1', currency="BTC", payment_method=payment_method.id)
        #print("Bought $" + str(user_amount_spent) + " or " + str(user_amount_spent / float(buy_price.amount)) + " bitcoin at " + buy_price.amount)
        
        #Within Purchase Threshold
        if(float(buy_price.amount) <= user_limit_order):
        # buy = client.buy(amount=str(user_amount_spent / float(buy_price.amount), currency=currency_code, payment_method=payment_method.id))
            print("Bought $" + str(user_amount_spent) + " or " + str(user_amount_spent / float(buy_price.amount)) + " bitcoin at " + buy_price.amount)
        
        sleep(60)
        #Update start_price
        start_price = buy_price

except AuthenticationError:
    print('Non è possibile Autentificarsi al tuo CoinBase Api.')
