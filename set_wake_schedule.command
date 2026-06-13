#!/bin/bash
echo "Setting daily 5:55am wake schedule..."
sudo pmset repeat wake MTWRFSU 05:55:00
echo ""
echo "Done. Verifying:"
pmset -g sched
echo ""
echo "Press any key to close."
read -n1
