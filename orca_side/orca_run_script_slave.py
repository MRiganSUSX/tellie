#!/usr/bin/env python
import argparse
import xmlrpclib
import time
from common import parameters as p

if __name__=="__main__":
    parser = argparse.ArgumentParser("Usage: orca_script.py <options>")
    parser.add_argument("-c", dest="channel", type=int, default=1, help="Select the TELLIE channel [1]")
    parser.add_argument("-n", dest="pulse_number", type=int, default=1, help="Set the number of pulses [1]")
    parser.add_argument("-t", dest="trigger_delay", type=int, default=0, help="Set the trigger delay [0]")
    parser.add_argument("-w", dest="pulse_width", type=int, default=p._max_pulse_width, help="Set the pulse width (intensity)")
    parser.add_argument("-z", dest="pulse_height", type=int, default=p._max_pulse_height, help="Set the pulse height (intensity)")
    parser.add_argument("-x", dest="fibre_delay", type=float, default=0, help="Set the individual fibre delay offset [0]")
    parser.add_argument("-s", dest="server", default="localhost", help="Server address to use [localhost]")
    parser.add_argument("-p", dest="port", default=p._server_port, help="Port number [5030]")
    args = parser.parse_args()

    tellie_server= xmlrpclib.ServerProxy('http://%s:%s' % (args.server, args.port))
    try:
        # TODO:
        # Parameter checks need to be performed here
        # But feedback needed for user (e.g. exact pulse number may not be possible)
        tellie_server.select_channel(args.channel)
        tellie_server.set_pulse_number(int(args.pulse_number))
        tellie_server.set_trigger_delay(int(args.trigger_delay))
        tellie_server.set_pulse_width(int(args.pulse_width))
        tellie_server.set_pulse_height(int(args.pulse_height))
        tellie_server.set_fibre_delay(float(args.fibre_delay))
        tellie_server.enable_external_trig()
        print "Trigger Averaged"
	tellie_server.trigger_averaged()
	try: 
	    print "Waiting for sequence to finish..."
            mean = None
            while (mean == None):
                try:
                    mean, rms, chan = tellie_server.read_pin_sequence()
                except TypeError:
                    mean = None
    	except xmlrpclib.Fault, e:
	    # Attempt a safe stop and inform in the return type as to the success?
	    tellie_server.stop()
    except xmlrpclib.Fault, e:
        # Attempt a safe stop and inform in the return type as to the success?
        print "Exception %s " % e
        tellie_server.stop()
    tellie_server.stop()
    tellie_server.clear_channel()
    print "Chan %s Mean %f RMS %f" %(chan,mean,rms)
        

