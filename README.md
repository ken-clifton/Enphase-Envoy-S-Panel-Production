# Enphase-Envoy-S-Panel-Production
Python v3 script to retrieve Enphase Envoy-S Solar Inverter Per-Panel Production

Please note that this script is NOT a product of Enphase Energy. If it doesn't work, please contact me, not Enphase. Enphase Energy is a company which primarily manufactures microinverters for solar PV arrays. Enphase Energy has an API for their Enlighten monitoring service. Enphase Enlighten (TM) provides access to current and historical solar production data and status informaton. Most of the power production information provided by this script is available through Enphase Enlighten via the Web, it just takes longer to retrieve.

The purpose of this script is to retrieve per-panel (inverter) information locally without traversing the Internet, or the need for the Enphase installer toolkit.

This Python script was created to run on Python 3.5 on most operating systems.
It has been tested on Pythonista version 3 on the iPad as well.

The script writes out a plain HTML file named: envoy-production.html , then opens that html in the local Web browser.
