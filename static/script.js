document.addEventListener("DOMContentLoaded", function() {
    console.log("Memulai pengambilan data jaringan...");
    fetch('http://127.0.0.1:5000/api/network-info') 
        .then(response => {
            console.log("Respons diterima:", response);
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            console.log("Data diterima:", data);
            if (data && data.ip_address) {
                document.getElementById('ip-address').textContent = data.ip_address;
            } else {
                document.getElementById('ip-address').textContent = 'IP Address tidak tersedia';
            }

            const wifiPasswordsList = document.getElementById('wifi-passwords');
            wifiPasswordsList.innerHTML = '';
            if (data && data.wifi_passwords && data.wifi_passwords.length > 0) {
                data.wifi_passwords.forEach(network => {
                    const li = document.createElement('li');
                    li.textContent = `SSID: ${network.ssid}, Password: ${network.password}`;
                    wifiPasswordsList.appendChild(li);
                });
            } else {
                wifiPasswordsList.innerHTML = '<li>Tidak ada informasi WiFi tersedia</li>';
            }
        })
        .catch(error => {
            console.error('Error saat mengambil info jaringan:', error);
            document.getElementById('ip-address').textContent = 'Gagal memuat IP Address';
            document.getElementById('wifi-passwords').innerHTML = '<li>Gagal memuat informasi WiFi</li>';
        });
});