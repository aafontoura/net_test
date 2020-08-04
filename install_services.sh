cp net_iperf_server.service /etc/systemd/system/
cp net_test.service /etc/systemd/system/

systemctl enable net_iperf_server.service
systemctl enable net_test.service

systemctl start net_iperf_server.service
systemctl start net_test.service