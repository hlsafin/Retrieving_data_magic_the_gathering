#!/usr/bin/python

import time;
import os;
from HTMLParser import HTMLParser
import urllib
import nltk;
import html2text;
import urllib2
import string;
import ctypes;
import shutil;

log_path = os.path.expanduser('~') + "\Desktop\log.txt"
with open(log_path, "a") as myfile:
    myfile.write("Update Price Bot Started...\n\n")

def getCardInfo(url):
    # The syntax is: SETNAME;CARDNAME;SELLING PRICE;FOIL SELLING PRICE;BUYING PRICE;FOIL BUYING PRICE;BUYING QUANTITY REGULAR;BUYING QUANTITY FOIL
    time.sleep(10)
    mhtml = urllib2.urlopen(url).readlines();
    buyer_str = "";
    seller_str = "";
    buyer_orig = "";
    seller_orig = "";
    buyers_flag = 0;
    sellers_flag = 0;
    name_str = "";
    set_str = "";
    buyer_float = 0.0;
    seller_float = 0.0;
    bot_name_seller = "";
    bot_name_buyer = "";

    bot_name_sec_seller = "";
    sell_price_sec_seller = "";

    sell_price_sec_seller_float = 0;
    seller_second_flag = 0;

    bot_name_sec_buyer = "";
    buy_price_sec_buyer = "";
    buy_price_sec_buyer_float = 0;
    buyer_second_flag = 0;

    tmp = url;
    arr = tmp.rsplit('/');
    tmp= arr[4]
    tmp= tmp.upper();
    set_str=tmp;
    for line in mhtml:
        if(line.__contains__("<td class=\"bot_name\">") and sellers_flag and line.__contains__("td")):
            if seller_second_flag == 0:
                bot_name_seller = string.replace(line,"<td class=\"bot_name\"><a href=\"javascript:void(0)\"><i class=\"fa fa-plus-square\"></i> ","");
                bot_name_seller = string.replace(bot_name_seller,"</a></td>","");
                bot_name_seller = string.replace(bot_name_seller,"<td class=\"bot_name\">","");
                bot_name_seller = string.replace(bot_name_seller,"</td>","");
                bot_name_seller = string.replace(bot_name_seller,"\n","");
                seller_second_flag = 1;
            elif seller_second_flag == 1:
                bot_name_sec_seller = string.replace(line,"<td class=\"bot_name\"><a href=\"javascript:void(0)\"><i class=\"fa fa-plus-square\"></i> ","");
                bot_name_sec_seller = string.replace(bot_name_sec_seller,"</a></td>","");
                bot_name_sec_seller = string.replace(bot_name_sec_seller,"<td class=\"bot_name\">","");
                bot_name_sec_seller = string.replace(bot_name_sec_seller,"</td>","");
                bot_name_sec_seller = string.replace(bot_name_sec_seller,"\n","");
                seller_second_flag = 2;

        if(line.__contains__("td class=\"sell_price_round")):
            our_str = line;
            if(sellers_flag == 1):
                if(seller_second_flag == 1):
                    our_str = string.replace(our_str,"<td class=\"sell_price_round\">","");
                    our_str = string.replace(our_str,"</td>","");
                    our_str = string.replace(our_str,"\n","");
                    seller_float = float(our_str);
                    our_str = '%.3f' % seller_float;
                    seller_str = our_str;
                    seller_orig = our_str;
                elif(seller_second_flag == 2):
                    our_str = string.replace(our_str,"<td class=\"sell_price_round\">","");
                    our_str = string.replace(our_str,"</td>","");
                    our_str = string.replace(our_str,"\n","");
                    sell_price_sec_seller_float = float(our_str);
                    our_str = '%.3f' % sell_price_sec_seller_float;
                    sell_price_sec_seller = our_str;
                    sellers_flag = 0;
                    seller_second_flag =3;

        if(line.__contains__("<td class=\"bot_name\">") and buyers_flag and line.__contains__("td")):
            if buyer_second_flag == 0:
                bot_name_buyer = string.replace(line,"<td class=\"bot_name\"><a href=\"javascript:void(0)\"><i class=\"fa fa-plus-square\"></i> ","");
                bot_name_buyer = string.replace(bot_name_buyer,"</a></td>","");
                bot_name_buyer = string.replace(bot_name_buyer,"<td class=\"bot_name\">","");
                bot_name_buyer = string.replace(bot_name_buyer,"</td>","");
                bot_name_buyer = string.replace(bot_name_buyer,"\n","");
                buyer_second_flag = 1;
            elif buyer_second_flag == 1:
                bot_name_sec_buyer = string.replace(line,"<td class=\"bot_name\"><a href=\"javascript:void(0)\"><i class=\"fa fa-plus-square\"></i> ","");
                bot_name_sec_buyer = string.replace(bot_name_sec_buyer,"</a></td>","");
                bot_name_sec_buyer = string.replace(bot_name_sec_buyer,"<td class=\"bot_name\">","");
                bot_name_sec_buyer = string.replace(bot_name_sec_buyer,"</td>","");
                bot_name_sec_buyer = string.replace(bot_name_sec_buyer,"\n","");
                buyer_second_flag = 2;

        if(line.__contains__("td class=\"buy_price_round")):
            our_str = line;
            if(buyers_flag == 1):
                if(buyer_second_flag == 1):
                    our_str = string.replace(our_str,"<td class=\"buy_price_round\">","");
                    our_str = string.replace(our_str,"</td>","");
                    our_str = string.replace(our_str,"\n","");
                    buyer_float = float(our_str);
                    our_str = '%.3f' % buyer_float;
                    buyer_str = our_str;
                    buyer_orig = our_str;
                elif(buyer_second_flag == 2):
                    our_str = string.replace(our_str,"<td class=\"buy_price_round\">","");
                    our_str = string.replace(our_str,"</td>","");
                    our_str = string.replace(our_str,"\n","");
                    buy_price_sec_buyer_float = float(our_str);
                    our_str = '%.3f' % buy_price_sec_buyer_float;
                    buy_price_sec_buyer = our_str;
                    buyers_flag = 0;
                    buyer_second_flag = 3;
                    break;

        if(line.__contains__("<title>")):
            name_str = string.replace(line," | MTGO Card Prices</title>","");
            name_str = string.replace(name_str,"<title>","");
            name_str = string.replace(name_str,"&#39;","'");
            name_str = string.replace(name_str,"\n","");

        if(line.__contains__("<h3>Sellers</h3>")):
            sellers_flag = 1;
            buyers_flag = 0;
        if(line.__contains__("<h3>Buyers</h3>")):
            sellers_flag = 0;
            buyers_flag = 1;

    buyer_float = float(buyer_str);
    seller_float = float(seller_str);

    if(bot_name_buyer == "memnarch1"):
        buyer_float = buy_price_sec_buyer_float;
    if(bot_name_seller == "memnarch1"):
        seller_float = sell_price_sec_seller_float;

    if(buyer_float > seller_float):
        temp = buyer_float;
        buyer_float = seller_float;
        seller_float = temp;
    else:
        buyer_float = buyer_float + 0.00;
        seller_float = seller_float - 0.000;

    buyer_str = "";
    buyer_str = '%.3f' % buyer_float;
    seller_str = "";
    seller_str = '%.3f' % seller_float;
    foil_sell_str = "";
    foil_buy_str = "";
    buy_qt_reg_str = "4";
    buy_qt_foil_str = "0"
    output = "";
    output = output + "Set: {}\n".format(set_str);
    output = output + "Name: {}\n".format(name_str);
    output = output + "{} \tSell Price (top):\t {}\n".format(bot_name_seller,seller_orig);
    output = output + "{} \tBuy Price (top):\t {}\n".format(bot_name_buyer,buyer_orig);
    output = output + "memnarch1 \tSell Price:\t\t {}\n".format(seller_str);
    output = output + "memnarch1 \tBuy Price:\t\t {}\n".format(buyer_str);
    # The syntax is: SETNAME;CARDNAME;SELLING PRICE;FOIL SELLING PRICE;BUYING PRICE;FOIL BUYING PRICE;BUYING QUANTITY REGULAR;BUYING QUANTITY FOIL
    pp_output = set_str + ";" + name_str + ";" + seller_str + ";" + foil_sell_str + ";" + buyer_str + ";" + foil_buy_str + ";" + buy_qt_reg_str + ";" + buy_qt_foil_str + "\n";
    output = output + pp_output;

    file_path = os.path.expanduser('~') + "\Desktop\PersonalPrices2.txt"
    if(not (os.path.exists(file_path))):
        print "{}: PersonalPricesRares.txt is not in {}".format(time.time(),file_path);
        return 1;
    writeout = ""
    with open(file_path, "r") as ins:
        array = []
        for line in ins:
            if(line.__contains__(name_str) == False):
                array.append(line);
                writeout = writeout + line;
        writeout = writeout + pp_output;
        array.append(str);

    f = open(file_path, "w");
    f.write(writeout);

    log_path = os.path.expanduser('~') + "\Desktop\log.txt"
    with open(log_path, "a") as myfile:
        myfile.write(output + "\n");
    print output;
    return output;

def updatePrice():
    file_path = os.path.expanduser('~') + "\Desktop\CardsURL3.txt"
    if(not (os.path.exists(file_path))):
        print "{}: CardsURL.txt is not in {}".format(time.time(),file_path);
        return 1;
    with open(file_path, "r") as ins:
        array = []
        for line in ins:
            if(line.__contains__("\n") == True):
                line = string.replace(line,"\n","");
            array.append(line);
    count = 0;
    skipped_urls = [];
    for str in array:
        count = count + 1;
        print "{}. {}".format(count,str);
        link = "{}. {}\n".format(count,str);
        log_path = os.path.expanduser('~') + "\Desktop\log.txt"
        with open(log_path, "a") as myfile:
            myfile.write(link)
        try:
            err = getCardInfo(str);
            if (isinstance(err,int) and err == 1):
                return 1;
        except ValueError:
            skipped_urls.append(str);
            print "ERROR!"


# manual start MTGO bot
# manual remove the PersonalPrices from lib
output = "";
while 1:
    # wait for 1 sec
    print "{}: Getting new price data...\n{}: (Total Process Time: 4 min and 10 sec / 35 cards)\n".format(time.time(),time.time());
    output = output + "{}: Getting new price data...\n{}: (Total Process Time: 4 min and 10 sec / 35 cards)\n\n".format(time.time(),time.time());
    time.sleep(2);

    # update the price (takes 5 min)
    err = updatePrice();
    if err:
        print "ERROR: Didn't locate needed files"
        break;
    print "{}: Got new updated PersonalPricesRares.txt @ Desktop".format(time.time());
    output = output + "{}: Got new updated PersonalPricesRares.txt @ Desktop\n".format(time.time());

    # wait for 1 sec
    time.sleep(2);

    # delete the PersonalPrices from mtgo lib
    if(os.path.exists("C:\Program Files (x86)\MTGOLibrary\MTGO Library Bot\prices\PersonalPrices2.txt")):
        os.remove("C:\Program Files (x86)\MTGOLibrary\MTGO Library Bot\prices\PersonalPrices2.txt");
        print "{}: PersonalPrices deleted @ MTGO Library Bot".format(time.time());
        output = output + "{}: PersonalPrices deleted @ MTGO Library Bot\n".format(time.time());

    # sleep for 1
    time.sleep(2);

    # copy PersonalPrices from Desktop to mtgo lib
    file_path = os.path.expanduser('~') + "\Desktop\PersonalPrices2.txt"
    if(os.path.exists(file_path)):
        shutil.copy(file_path,'C:\Program Files (x86)\MTGOLibrary\MTGO Library Bot\prices\PersonalPrices2.txt');
        print "{}: PersonalPrices copied to MTGO Library Bot from {}".format(time.time(),file_path);
        output = output + "{}: PersonalPrices copied to MTGO Library Bot from {}\n".format(time.time(),file_path);

    # wait 5 min for the mtgo get the new price from lib
    print "{}: Passing PersonalPricesRares.txt to MTGO Bot...".format(time.time());
    output = output + "{}: Passing PersonalPricesRares.txt to MTGO Bot...\n".format(time.time());
    time.sleep(60)
    print "{}: Prices should be updated on MTGO".format(time.time());
    output = output + "{}: Prices should be updated on MTGO\n".format(time.time());
    time.sleep(180)
    print "{}: Updating price starts in 60 sec".format(time.time());
    output = output + "{}: Updating price starts in 60 sec\n".format(time.time());
    time.sleep(60)
    #log_path = os.path.expanduser('~') + "\Desktop\log.txt"
    #with open(log_path, "a") as myfile:
     #   myfile.write(output + "\n")
