cd /home/spgir_auto
source venv/bin/activate
echo 2 | nohup python sc.py > main_logs/$(date "+%Y_%m_%d_%H_%M_%S").out &