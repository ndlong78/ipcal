 (cd "$(git rev-parse --show-toplevel)" && git apply --3way <<'EOF' 
diff --git a/app/calculations.py b/app/calculations.py
index 5269f30e5e288ec6210c1b2baf08ce5a09db234c..c0e52603d231f6181cfe4ef26a716b7cdcd17102 100644
--- a/app/calculations.py
+++ b/app/calculations.py
@@ -43,76 +43,94 @@ def calculate_ipv6(ip_address):
 
 def calculate_ipv4_network_and_subnet(ip_address, network_input):
     """
     Calculate network and subnet details for IPv4.
 
     Args:
         ip_address (str): The IPv4 address.
         network_input (str): The network input in CIDR or Netmask format.
 
     Returns:
         dict: Dictionary containing network and subnet details or error message.
     """
     try:
         if re.match(r'^\d{1,2}$', network_input) and 0 <= int(network_input) <= 32:
             # Input is in CIDR prefix length format (e.g., "24")
             network = ipaddress.IPv4Network(f"{ip_address}/{network_input}", strict=False)
         elif re.match(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$', network_input):
             # Input is in netmask format (e.g., "255.255.255.0")
             ip = ipaddress.IPv4Interface(f"{ip_address}/{network_input}")
             network = ip.network
         else:
             return {"error": "Invalid network input. Please enter a valid CIDR or Netmask."}
         
         # Calculate Wildcard, HostMin, HostMax
         wildcard = str(ipaddress.IPv4Address(int(network.hostmask)))
-        host_min = str(network.network_address + 1)
-        host_max = str(network.broadcast_address - 1)
-        
+
+        total_addresses = network.num_addresses
+        if network.prefixlen == 32:
+            host_min = host_max = str(network.network_address)
+            usable_hosts = 1
+        elif network.prefixlen == 31:
+            host_min = str(network.network_address)
+            host_max = str(network.broadcast_address)
+            usable_hosts = 2
+        else:
+            host_min = str(network.network_address + 1)
+            host_max = str(network.broadcast_address - 1)
+            usable_hosts = max(total_addresses - 2, 0)
+
         return {
             "Network Address": str(network.network_address),
             "CIDR": str(network.prefixlen),
             "Netmask": str(network.netmask),
             "Wildcard": wildcard,
             "HostMin": host_min,
             "HostMax": host_max,
-            "Total Hosts": network.num_addresses - 2  # Subtract network and broadcast addresses
+            "Total Hosts": usable_hosts
         }
     except ValueError:
         return {"error": "Invalid network"}
 
 def calculate_ipv6_network_and_subnet(ip_address, network_input):
     """
     Calculate network and subnet details for IPv6.
 
     Args:
         ip_address (str): The IPv6 address.
         network_input (str): The network input in CIDR or Netmask format.
 
     Returns:
         dict: Dictionary containing network and subnet details or error message.
     """
     try:
         if re.match(r'^\d{1,3}$', network_input) and 0 <= int(network_input) <= 128:
             # Input is in CIDR prefix length format (e.g., "64")
             network = ipaddress.IPv6Network(f"{ip_address}/{network_input}", strict=False)
         elif ':' in network_input:
             # Input is in netmask format (e.g., "ffff:ffff:ffff:ffff::")
             ip = ipaddress.IPv6Interface(f"{ip_address}/{network_input}")
             network = ip.network
         else:
             return {"error": "Invalid network input. Please enter a valid CIDR or Netmask."}
         
         # Calculate HostMin, HostMax
-        host_min = str(network.network_address + 1)
-        host_max = str(network.broadcast_address - 1)
-        
+        total_addresses = network.num_addresses
+        if total_addresses == 1:
+            host_min = host_max = str(network.network_address)
+        elif network.prefixlen == 127:
+            host_min = str(network.network_address)
+            host_max = str(network.broadcast_address)
+        else:
+            host_min = str(network.network_address + 1)
+            host_max = str(network.broadcast_address - 1)
+
         return {
             "Network Address": str(network.network_address),
             "CIDR": str(network.prefixlen),
             "Netmask": str(network.netmask),
             "HostMin": host_min,
             "HostMax": host_max,
             "Total Hosts": network.num_addresses  # No need to subtract for IPv6
         }
     except ValueError:
-        return {"error": "Invalid network"}
+        return {"error": "Invalid network"}
 
EOF
)
