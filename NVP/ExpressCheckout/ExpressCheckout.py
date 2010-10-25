#! /usr/bin/python

# Requires the httplib2 library to be installed
# Tested using Python 2.6.3

__author__="jv"

import urllib
import httplib2
import urlparse


class ExpressCheckout:


    def __init__(self):
        self.httpObject = httplib2.Http()
        self.sandbox = 'https://api-3t.sandbox.paypal.com/nvp'
        self.live = 'https://api-3t.paypal.com/nvp'
        self.credentials={
            'USER': '' ,
            'PWD': '',
            'SIGNATURE': '',
            'VERSION':"63.0",
            }
        self.parameters = {                        
            'RETURNURL':"<insert URL>",
            'CANCELURL':"<insert URL>",
            
        }

    def setExpressCheckout(self, ecParams,liveOrSandbox="sandbox"):       
        postData = urllib.urlencode(self.parameters)+"&"+urllib.urlencode(ecParams)
        resp, content = self.postToPayPal(postData)

        return urlparse.parse_qs(urllib.unquote(content))['TOKEN'][0]

    def postToPayPal(self,postData,liveOrSandbox="sandbox"):
        url=self.sandbox
        if liveOrSandbox.lower().strip()=="live" :
            url=self.live
        return self.httpObject.request(url,method="POST",
                                    body=urllib.urlencode(self.credentials)+"&"+postData,
                                    headers={'cache-control':'no-cache','Content-type':'application/x-www-form-urlencoded'})

    def getExpressCheckoutDetails(self,token):
        resp, content = self.postToPayPal("&METHOD=GetExpressCheckoutDetails&TOKEN="+token)
        return urlparse.parse_qs(content)
    
    def doExpressCheckout(self,params):
        resp, content = self.postToPayPal(urllib.urlencode(params))
        return urlparse.parse_qs(content)
        

if __name__ == "__main__":
    ec = ExpressCheckout()
    #test SetExpressCheckout
    if False: #change to true to run test
        setEcVars={
                'PAYMENTREQUEST_0_PAYMENTACTION':"Sale", #Authorization,Order
                'CURRENCYCODE':"USD",
                'PAYMENTREQUEST_0_AMT':"1,000",
                'METHOD':'SetExpressCheckout',
                'PAYMENTREQUEST_0_SHIPTONAME':'xxx',
                'PAYMENTREQUEST_0_SHIPTOSTREET':'xxx',
                'PAYMENTREQUEST_0_SHIPTOCITY':'xxx',
                'PAYMENTREQUEST_0_SHIPTOCOUNTRYCODE':'US',
                'PAYMENTREQUEST_0_SHIPTOZIP': 'xxx',
                'L_NAME0':"TEST NAME"
                
                
                }
        token= ec.setExpressCheckout(setEcVars)
        print "Redirect browser to :"
        print "https://www.sandbox.paypal.com/cgi-bin/webscr?cmd=_express-checkout&token="+token
        

    #test DoExpressCheckoutPayment
    if True :
        doECParams={
            "METHOD" :"DoExpressCheckoutPayment",
            "PAYMENTREQUEST_0_PAYMENTACTION":"Sale",
            "PAYERID" :"",
            "TOKEN" : "EC-xxx", #token,
            "PAYMENTREQUEST_0_AMT" : "19.95",
            'PAYMENTREQUEST_0_SHIPTONAME':'test',
            'PAYMENTREQUEST_0_SHIPTOSTREET':'123 main',
            'PAYMENTREQUEST_0_SHIPTOCITY':'San Jose',
            'PAYMENTREQUEST_0_SHIPTOSTATE':'CA',
            'PAYMENTREQUEST_0_SHIPTOCOUNTRYCODE':'US',
            'PAYMENTREQUEST_0_SHIPTOZIP': '95101'
            }
        print ec.doExpressCheckout(doECParams)
        
    if True:
        print ec.getExpressCheckoutDetails("EC-xxx")
    
