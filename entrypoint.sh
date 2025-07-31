#!/bin/sh

# Block all outbound internet access
iptables -A OUTPUT -d 0.0.0.0/0 -j DROP

# Start the Flask app
python3 run.py
