#!/usr/bin/env python
# -*- coding: utf-8 -*-


###################################################################
#                                                                 #
#                                                                 #
#                                                                 #
#                                                                 #
#                        Packages import                          #
#                                                                 #
#                                                                 #
#                                                                 #
###################################################################

from telegram.ext import Updater, CommandHandler, MessageHandler
from emoji import emojize
from apscheduler.schedulers.blocking import BlockingScheduler
import threading
from threading import Thread






###################################################################
#                                                                 #
#                                                                 #
#                                                                 #
#                                                                 #
#                        Function import                          #
#                                                                 #
#                                                                 #
#                                                                 #
###################################################################

from arbitrage_test import arbitrage




###################################################################
#                                                                 #
#                                                                 #
#                                                                 #
#                                                                 #
#                       Global variables                          #
#                                                                 #
#                                                                 #
#                                                                 #
###################################################################

Thread_simple_arbitrage = None
Thread_triangular_arbitrage = None




###################################################################
#                                                                 #
#                                                                 #
#                                                                 #
#                                                                 #
#              Custom stoppable thread class                      #
#                                                                 #
#                                                                 #
#                                                                 #
###################################################################

class StoppableThread(threading.Thread):
    
    # Constructor, setting initial variables
    def __init__(self, function):
        self._function = function
        self._stopevent = threading.Event()
        threading.Thread.__init__(self)
    
    # Main loop
    def run(self):
        while not self._stopevent.isSet():
            self._function(self)
    
    # Give the order to stop the thread
    def stop(self):
        self._stopevent.set()
    
    # Return True if the user requested to stop the thread
    def stopped(self):
        return self._stopevent.isSet()





###################################################################
#                                                                 #
#                                                                 #
#                                                                 #
#                                                                 #
#                     Telegram bot command                        #
#                                                                 #
#                                                                 #
#                                                                 #
###################################################################

def start(bot, update):
    update.message.reply_text('Hi, I\'m the cryptocurrencies arbitrage bot! '+ 
                              emojize(":wave:", use_aliases=True)+
                              "\nCheck the command /help to know what I can do for you.")
def non_command(bot, update):
    update.message.reply_text("Sorry, but I did'nt understood your query.\n"+
                              "Please check the command /help to know what I can do for you.")

def begin_simple_arbitrage(bot, update):
    global Thread_simple_arbitrage
    if(Thread_simple_arbitrage == None):
        Thread_simple_arbitrage = StoppableThread(arbitrage)
        Thread_simple_arbitrage.start()
        update.message.reply_text("The simple arbitrage script has been launched.")
    else:
        update.message.reply_text("Error : the simple arbitrage script is already launched.")

def stop_simple_arbitrage(bot, update):
    global Thread_simple_arbitrage
    if(Thread_simple_arbitrage == None):
        Thread_simple_arbitrage.stop()
        update.message.reply_text("The simple arbitrage script has been stopped.")
    else:
        update.message.reply_text("Error : the simple arbitrage script is not running.")



###################################################################
#                                                                 #
#                                                                 #
#                                                                 #
#                                                                 #
#                       Scheduler function                        #
#                                                                 #
#                                                                 #
#                                                                 #
###################################################################

def SendNewsletter(bot):
    id_client = 309106884
    bot.sendMessage(id_client, "ok")

def ThreadFunctionScheduler(bot):
    scheduler = BlockingScheduler()
    scheduler.add_job(SendNewsletter, 'interval', hours=1, args=(bot,))
    scheduler.start()

def ThreadBot(updater):
    updater.start_polling()




###################################################################
#                                                                 #
#                                                                 #
#                                                                 #
#                                                                 #
#                            Main                                 #
#                                                                 #
#                                                                 #
#                                                                 #
###################################################################
    
def main():
    # Create the EventHandler and pass it your bot's token.
    updater = Updater("386765167:AAEAeiO5sgg5AjlQFIw6OiYWTXr1qBeQsrE")
    
    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("begin_simple_arbitrage", begin_simple_arbitrage))
    dp.add_handler(CommandHandler("stop_simple_arbitrage", stop_simple_arbitrage))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, non_command))
    
    #Start scheduler
    t1 = Thread(target=ThreadFunctionScheduler, args=(updater.bot,))
    t1.start()
    # Start the Bot
    t2 = Thread(target=ThreadBot, args=(updater,))
    t2.start()
    
    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()