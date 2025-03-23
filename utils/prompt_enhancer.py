#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import psutil
import platform
import requests
import pytz
from datetime import datetime
import socket
import uuid
import os
import locale
import time
import subprocess
import pwd
from collections import defaultdict

class PromptEnhancer:
    def __init__(self, logger):
        """
        Initialize the prompt enhancer

        Args:
            logger: Logger instance to log events
        """
        self.logger = logger

    def enhance_prompt(self, base_prompt, enhancements):
        """
        Enhance a prompt with additional information

        Args:
            base_prompt: The base prompt
            enhancements: List of enhancements to apply

        Returns:
            str: The enhanced prompt
        """
        info_sections = []

        all_enhancements = [
            "time", "system", "network", "locale", "timezone",
            "performance", "hardware", "users", "network_traffic",
            "ports", "processes", "filesystem", "services"
        ]

        if enhancements == "all" or "all" in enhancements:
            enhancements_to_apply = all_enhancements
        else:
            enhancements_to_apply = enhancements

        for enhancement in enhancements_to_apply:
            if enhancement == "time":
                time_info = self.get_current_time_info()
                if time_info:
                    info_sections.append(f"Current time: {time_info['full']}")
                    info_sections.append(f"UTC time: {time_info['utc']}")

            elif enhancement == "system":
                sys_info = self.get_system_info()
                if sys_info:
                    info_sections.append(f"System: {sys_info['os']} {sys_info['version']}")
                    info_sections.append(f"CPU: {sys_info['cpu_model']} ({sys_info['cpu_cores']} cores, {sys_info['cpu']}% usage)")
                    info_sections.append(f"RAM: {sys_info['memory_gb']}GB total, {sys_info['memory']}% used")
                    info_sections.append(f"Disk: {sys_info['disk_total']}GB total, {sys_info['disk_percent']}% used")
                    info_sections.append(f"System uptime: {sys_info['uptime']}")

            elif enhancement == "network":
                network_info = self.get_network_info()
                if network_info:
                    info_sections.append(f"Network: IP {network_info['local_ip']}, hostname {network_info['hostname']}")
                    info_sections.append(f"Network interfaces: {', '.join(network_info['interfaces'])}")
                    if network_info['internet_available']:
                        info_sections.append(f"Internet connection: Available (latency: {network_info['latency']}ms)")
                    else:
                        info_sections.append("Internet connection: Unavailable")

            elif enhancement == "locale":
                locale_info = self.get_locale_info()
                if locale_info:
                    info_sections.append(f"System locale: {locale_info['language']}, {locale_info['encoding']}")
                    info_sections.append(f"Currency: {locale_info['currency']}")
                    info_sections.append(f"Time format: {locale_info['time_format']}")
                    info_sections.append(f"Date format: {locale_info['date_format']}")

            elif enhancement == "timezone":
                timezone_info = self.get_timezone_info()
                if timezone_info:
                    info_sections.append(f"Timezone information:")
                    info_sections.append(f"  Current timezone: {timezone_info['current']}")
                    info_sections.append(f"  UTC offset: {timezone_info['utc_offset']}")
                    info_sections.append(f"  DST active: {timezone_info['dst_active']}")

            elif enhancement == "performance":
                perf_info = self.get_performance_metrics()
                if perf_info:
                    info_sections.append("System performance:")
                    info_sections.append(f"  CPU load: 1min: {perf_info['load_1']}, 5min: {perf_info['load_5']}, 15min: {perf_info['load_15']}")
                    info_sections.append(f"  Process count: {perf_info['process_count']}")
                    info_sections.append(f"  Network usage: {perf_info['network_sent']}MB sent, {perf_info['network_recv']}MB received")
                    info_sections.append(f"  Swap usage: {perf_info['swap_percent']}%")

            elif enhancement == "hardware":
                hw_info = self.get_hardware_info()
                if hw_info:
                    info_sections.append("Hardware information:")
                    info_sections.append(f"  Machine type: {hw_info['machine_type']}")
                    info_sections.append(f"  Processor: {hw_info['processor']}")
                    info_sections.append(f"  BIOS version: {hw_info['bios_version']}")
                    info_sections.append(f"  Boot mode: {hw_info['boot_mode']}")

            elif enhancement == "users":
                users_info = self.get_users_info()
                if users_info:
                    info_sections.append("Users information:")
                    info_sections.append(f"  Logged in users: {users_info['logged_users_count']}")
                    users_list = ", ".join(users_info['logged_users'][:5])
                    if len(users_info['logged_users']) > 5:
                        users_list += f" and {len(users_info['logged_users']) - 5} more"
                    info_sections.append(f"  Current users: {users_list}")
                    info_sections.append(f"  System users: {users_info['system_users_count']}")
                    info_sections.append(f"  User sessions: {users_info['sessions_count']}")

            elif enhancement == "network_traffic":
                traffic_info = self.get_network_traffic()
                if traffic_info:
                    info_sections.append("Network traffic:")
                    info_sections.append(f"  Current download speed: {traffic_info['download_speed']} KB/s")
                    info_sections.append(f"  Current upload speed: {traffic_info['upload_speed']} KB/s")
                    info_sections.append(f"  Total downloaded: {traffic_info['total_received']} MB")
                    info_sections.append(f"  Total uploaded: {traffic_info['total_sent']} MB")
                    info_sections.append(f"  Packets received: {traffic_info['packets_recv']}")
                    info_sections.append(f"  Packets sent: {traffic_info['packets_sent']}")

            elif enhancement == "ports":
                ports_info = self.get_open_ports()
                if ports_info:
                    info_sections.append("Open ports and connections:")
                    info_sections.append(f"  Total connections: {ports_info['total_connections']}")
                    info_sections.append(f"  Listening ports: {', '.join(map(str, ports_info['listening_ports'][:10]))}")
                    if len(ports_info['listening_ports']) > 10:
                        info_sections.append(f"    and {len(ports_info['listening_ports']) - 10} more...")
                    info_sections.append(f"  Established connections: {ports_info['established']}")
                    info_sections.append(f"  Top processes using network: {', '.join(ports_info['top_processes'])}")

            elif enhancement == "processes":
                processes_info = self.get_process_info()
                if processes_info:
                    info_sections.append("Process information:")
                    info_sections.append(f"  Total processes: {processes_info['total']}")
                    info_sections.append(f"  Running processes: {processes_info['running']}")
                    info_sections.append(f"  Top CPU processes: {', '.join(processes_info['top_cpu'])}")
                    info_sections.append(f"  Top memory processes: {', '.join(processes_info['top_memory'])}")

            elif enhancement == "filesystem":
                fs_info = self.get_filesystem_info()
                if fs_info:
                    info_sections.append("Filesystem information:")
                    for disk in fs_info['disks'][:3]:
                        info_sections.append(f"  {disk['device']}: {disk['mountpoint']}, {disk['fstype']}, {disk['total_gb']}GB total, {disk['percent']}% used")
                    if len(fs_info['disks']) > 3:
                        info_sections.append(f"  ... and {len(fs_info['disks']) - 3} more filesystems")
                    info_sections.append(f"  Total file operations: {fs_info['io_read']} reads, {fs_info['io_write']} writes")

            elif enhancement == "services":
                services_info = self.get_services_info()
                if services_info:
                    info_sections.append("System services:")
                    info_sections.append(f"  Running services: {services_info['running_count']}")
                    info_sections.append(f"  Critical services: {', '.join(services_info['critical'][:5])}")
                    if len(services_info['critical']) > 5:
                        info_sections.append(f"    ... and {len(services_info['critical']) - 5} more")

        if info_sections:
            info_text = "\n".join(info_sections)
            enriched_prompt = f"{base_prompt}\n\nHere is real-time information you can use if relevant:\n{info_text}\n\nThe email is:"
            return enriched_prompt

        return base_prompt

    def get_current_time_info(self):
        """
        Retrieve current date and time information

        Returns:
            dict: Date and time information
        """
        now_local = datetime.now()
        now_utc = datetime.utcnow()

        # Detect local timezone
        local_tz = time.tzname[0]

        weekday = now_local.strftime('%A')
        date = now_local.strftime('%d %B %Y')
        time_str = now_local.strftime('%H:%M:%S')

        return {
            "weekday": weekday,
            "date": date,
            "time": time_str,
            "full": f"{weekday}, {date} {time_str} ({local_tz})",
            "utc": now_utc.strftime('%Y-%m-%d %H:%M:%S UTC'),
            "timestamp": int(time.time())
        }

    def get_system_info(self):
        """
        Retrieve detailed system information

        Returns:
            dict: System information or None in case of error
        """
        try:
            # OS info
            os_name = platform.system()
            os_version = platform.release()

            # CPU info
            cpu_usage = psutil.cpu_percent(interval=1)
            cpu_cores = psutil.cpu_count(logical=True)
            cpu_physical = psutil.cpu_count(logical=False)

            try:
                if platform.system() == "Windows":
                    cpu_model = platform.processor()
                else:
                    cmd = "cat /proc/cpuinfo | grep 'model name' | uniq"
                    cpu_model = subprocess.check_output(cmd, shell=True).decode().strip().split(":")[1].strip()
            except:
                cpu_model = "Unknown CPU"

            # Memory info
            memory = psutil.virtual_memory()
            memory_used_percent = memory.percent
            memory_total_gb = round(memory.total / (1024**3), 2)

            # Disk info
            disk = psutil.disk_usage('/')
            disk_total = round(disk.total / (1024**3), 2)
            disk_percent = disk.percent

            # Uptime
            boot_time = datetime.fromtimestamp(psutil.boot_time())
            uptime = datetime.now() - boot_time
            uptime_days = uptime.days
            uptime_hours = uptime.seconds // 3600
            uptime_minutes = (uptime.seconds // 60) % 60

            return {
                "os": os_name,
                "version": os_version,
                "cpu": cpu_usage,
                "cpu_cores": cpu_cores,
                "physical_cores": cpu_physical,
                "cpu_model": cpu_model,
                "memory": memory_used_percent,
                "memory_gb": memory_total_gb,
                "disk_total": disk_total,
                "disk_percent": disk_percent,
                "uptime": f"{uptime_days} days, {uptime_hours} hours, {uptime_minutes} minutes"
            }
        except Exception as e:
            self.logger.log_message(f"Error getting system info: {str(e)}")
            return None

    def get_network_info(self):
        """
        Retrieve network information

        Returns:
            dict: Network information or None in case of error
        """
        try:
            # Hostname
            hostname = socket.gethostname()

            # Local IP
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            try:
                # Does not actually connect
                s.connect(('10.255.255.255', 1))
                local_ip = s.getsockname()[0]
            except Exception:
                local_ip = '127.0.0.1'
            finally:
                s.close()

            # MAC address
            mac = ':'.join(['{:02x}'.format((uuid.getnode() >> ele) & 0xff) for ele in range(0, 8*6, 8)][::-1])

            # Network interfaces
            interfaces = []
            for iface, addrs in psutil.net_if_addrs().items():
                interfaces.append(iface)

            # Test internet connection
            internet_available = False
            latency = -1
            try:
                start = time.time()
                requests.get('https://www.google.com', timeout=2)
                latency = round((time.time() - start) * 1000, 2)
                internet_available = True
            except:
                pass

            return {
                "hostname": hostname,
                "local_ip": local_ip,
                "mac_address": mac,
                "interfaces": interfaces,
                "internet_available": internet_available,
                "latency": latency
            }
        except Exception as e:
            self.logger.log_message(f"Error getting network info: {str(e)}")
            return None

    def get_locale_info(self):
        """
        Retrieve system locale information

        Returns:
            dict: Locale information or None in case of error
        """
        try:
            current_locale = locale.getlocale()

            # Try to retrieve formats
            try:
                locale.setlocale(locale.LC_ALL, '')
                currency_symbol = locale.localeconv()['currency_symbol']
                time_format = time.strftime('%X')
                date_format = time.strftime('%x')
            except:
                currency_symbol = "Unknown"
                time_format = "Unknown"
                date_format = "Unknown"

            return {
                "language": current_locale[0] if current_locale[0] else "Unknown",
                "encoding": current_locale[1] if current_locale[1] else "Unknown",
                "currency": currency_symbol,
                "time_format": time_format,
                "date_format": date_format
            }
        except Exception as e:
            self.logger.log_message(f"Error getting locale info: {str(e)}")
            return None

    def get_timezone_info(self):
        """
        Retrieve detailed timezone information

        Returns:
            dict: Timezone information or None in case of error
        """
        try:
            # Local timezone
            local_zone = time.tzname[0]

            # UTC offset (in hours)
            utc_offset = round(time.timezone / -3600, 2)
            if time.daylight and time.localtime().tm_isdst > 0:
                utc_offset = round(time.altzone / -3600, 2)

            # DST (Daylight Saving Time)
            is_dst = bool(time.localtime().tm_isdst)

            # List of available timezones
            available_timezones = pytz.all_timezones[:5]  # Just a few examples

            return {
                "current": local_zone,
                "utc_offset": f"{utc_offset:+g} hours",
                "dst_active": is_dst,
                "examples": available_timezones
            }
        except Exception as e:
            self.logger.log_message(f"Error getting timezone info: {str(e)}")
            return None

    def get_performance_metrics(self):
        """
        Retrieve system performance metrics

        Returns:
            dict: Performance metrics or None in case of error
        """
        try:
            # System load
            load_1, load_5, load_15 = os.getloadavg() if hasattr(os, 'getloadavg') else (-1, -1, -1)

            # Number of processes
            process_count = len(psutil.pids())

            # Network usage
            net_io = psutil.net_io_counters()
            net_sent = round(net_io.bytes_sent / (1024**2), 2)  # MB
            net_recv = round(net_io.bytes_recv / (1024**2), 2)  # MB

            # Swap memory
            swap = psutil.swap_memory()
            swap_percent = swap.percent

            # Process start times
            boot_time = datetime.fromtimestamp(psutil.boot_time())

            return {
                "load_1": load_1,
                "load_5": load_5,
                "load_15": load_15,
                "process_count": process_count,
                "network_sent": net_sent,
                "network_recv": net_recv,
                "swap_percent": swap_percent,
                "boot_time": boot_time.strftime("%Y-%m-%d %H:%M:%S")
            }
        except Exception as e:
            self.logger.log_message(f"Error getting performance metrics: {str(e)}")
            return None

    def get_hardware_info(self):
        """
        Retrieve hardware information

        Returns:
            dict: Hardware information or None in case of error
        """
        try:
            machine_type = platform.machine()
            processor = platform.processor()

            bios_version = "Unknown"
            if platform.system() == "Windows":
                try:
                    import wmi
                    c = wmi.WMI()
                    for bios in c.Win32_BIOS():
                        bios_version = bios.Version
                except:
                    pass

            boot_mode = "Unknown"
            if platform.system() == "Linux":
                try:
                    if os.path.exists('/sys/firmware/efi'):
                        boot_mode = "UEFI"
                    else:
                        boot_mode = "Legacy BIOS"
                except:
                    pass

            return {
                "machine_type": machine_type,
                "processor": processor,
                "bios_version": bios_version,
                "boot_mode": boot_mode
            }
        except Exception as e:
            self.logger.log_message(f"Error getting hardware info: {str(e)}")
            return None

    def get_users_info(self):
        """
        Retrieve system user information

        Returns:
            dict: User information or None in case of error
        """
        try:
            # Logged-in users
            logged_users = []
            sessions_count = 0
            try:
                for user in psutil.users():
                    logged_users.append(user.name)
                    sessions_count += 1
            except:
                # Alternative method for Unix
                try:
                    output = subprocess.check_output(["who"]).decode()
                    for line in output.split('\n'):
                        if line.strip():
                            username = line.split()[0]
                            if username not in logged_users:
                                logged_users.append(username)
                            sessions_count += 1
                except:
                    pass

            # All system users
            system_users = []
            try:
                if platform.system() != "Windows":
                    # Unix method
                    for p in pwd.getpwall():
                        system_users.append(p[0])
                else:
                    # Windows method
                    output = subprocess.check_output(["net", "user"]).decode()
                    for line in output.split('\n'):
                        line = line.strip()
                        if line and not line.startswith('-') and not line.startswith('User accounts') and not line.startswith('The command'):
                            users = line.split()
                            system_users.extend(users)
            except:
                pass

            return {
                "logged_users": logged_users,
                "logged_users_count": len(logged_users),
                "system_users": system_users,
                "system_users_count": len(system_users),
                "sessions_count": sessions_count
            }
        except Exception as e:
            self.logger.log_message(f"Error getting users info: {str(e)}")
            return None

    def get_network_traffic(self):
        """
        Retrieve current network traffic information

        Returns:
            dict: Network traffic information or None in case of error
        """
        try:
            # First measurement
            net_io1 = psutil.net_io_counters()

            # Wait a bit to calculate speed
            time.sleep(1)

            # Second measurement
            net_io2 = psutil.net_io_counters()

            # Calculate speed
            download_speed = round((net_io2.bytes_recv - net_io1.bytes_recv) / 1024, 2)  # KB/s
            upload_speed = round((net_io2.bytes_sent - net_io1.bytes_sent) / 1024, 2)    # KB/s

            # Totals
            total_sent = round(net_io2.bytes_sent / (1024 * 1024), 2)     # MB
            total_received = round(net_io2.bytes_recv / (1024 * 1024), 2) # MB

            # Other statistics
            packets_sent = net_io2.packets_sent
            packets_recv = net_io2.packets_recv

            # Statistics per interface
            interfaces_stats = {}
            try:
                for iface, stats in psutil.net_io_counters(pernic=True).items():
                    if_sent = round(stats.bytes_sent / (1024 * 1024), 2)  # MB
                    if_recv = round(stats.bytes_recv / (1024 * 1024), 2)  # MB
                    interfaces_stats[iface] = {
                        "sent_mb": if_sent,
                        "received_mb": if_recv,
                        "packets_sent": stats.packets_sent,
                        "packets_recv": stats.packets_recv
                    }
            except:
                pass

            return {
                "download_speed": download_speed,
                "upload_speed": upload_speed,
                "total_sent": total_sent,
                "total_received": total_received,
                "packets_sent": packets_sent,
                "packets_recv": packets_recv,
                "interfaces": interfaces_stats
            }
        except Exception as e:
            self.logger.log_message(f"Error getting network traffic: {str(e)}")
            return None

    def get_open_ports(self):
        """
        Retrieve information about open ports and network connections

        Returns:
            dict: Ports and connections information or None in case of error
        """
        try:
            connections = psutil.net_connections()

            # Listening ports
            listening_ports = []
            established = 0
            process_connections = defaultdict(int)

            for conn in connections:
                # Listening ports (servers)
                if conn.status == 'LISTEN' and conn.laddr.port not in listening_ports:
                    listening_ports.append(conn.laddr.port)

                # Established connections
                if conn.status == 'ESTABLISHED':
                    established += 1

                # Count per process
                if conn.pid:
                    try:
                        proc = psutil.Process(conn.pid)
                        process_connections[proc.name()] += 1
                    except:
                        pass

            # Top processes by number of connections
            top_processes = []
            for proc, count in sorted(process_connections.items(), key=lambda x: x[1], reverse=True)[:5]:
                top_processes.append(f"{proc} ({count})")

            # Alternative method for Linux
            if not listening_ports and platform.system() == "Linux":
                try:
                    output = subprocess.check_output(["netstat", "-tuln"]).decode()
                    for line in output.split('\n'):
                        if "LISTEN" in line:
                            parts = line.split()
                            if len(parts) >= 4:
                                addr = parts[3]
                                port = addr.split(':')[-1]
                                try:
                                    port_num = int(port)
                                    if port_num not in listening_ports:
                                        listening_ports.append(port_num)
                                except:
                                    pass
                except:
                    pass

            return {
                "listening_ports": sorted(listening_ports),
                "total_connections": len(connections),
                "established": established,
                "top_processes": top_processes
            }
        except Exception as e:
            self.logger.log_message(f"Error getting open ports: {str(e)}")
            return None

    def get_process_info(self):
        """
        Retrieve information about running processes

        Returns:
            dict: Process information or None in case of error
        """
        try:
            procs = []
            running_count = 0

            for proc in psutil.process_iter(['pid', 'name', 'username', 'status', 'cpu_percent', 'memory_percent']):
                try:
                    pinfo = proc.info
                    procs.append(pinfo)
                    if pinfo['status'] == 'running':
                        running_count += 1
                except:
                    pass

            # Sort by CPU usage
            top_cpu = []
            for p in sorted(procs, key=lambda p: p.get('cpu_percent', 0), reverse=True)[:5]:
                if p.get('cpu_percent', 0) > 0:
                    top_cpu.append(f"{p['name']} ({p['cpu_percent']:.1f}%)")

            # Sort by memory usage
            top_memory = []
            for p in sorted(procs, key=lambda p: p.get('memory_percent', 0), reverse=True)[:5]:
                if p.get('memory_percent', 0) > 0:
                    top_memory.append(f"{p['name']} ({p['memory_percent']:.1f}%)")

            return {
                "total": len(procs),
                "running": running_count,
                "top_cpu": top_cpu,
                "top_memory": top_memory
            }
        except Exception as e:
            self.logger.log_message(f"Error getting process info: {str(e)}")
            return None

    def get_filesystem_info(self):
        """
        Retrieve detailed filesystem information

        Returns:
            dict: Filesystem information or None in case of error
        """
        try:
            # Disk information
            disks = []
            for partition in psutil.disk_partitions():
                try:
                    usage = psutil.disk_usage(partition.mountpoint)
                    disks.append({
                        "device": partition.device,
                        "mountpoint": partition.mountpoint,
                        "fstype": partition.fstype,
                        "total_gb": round(usage.total / (1024**3), 2),
                        "used_gb": round(usage.used / (1024**3), 2),
                        "percent": usage.percent
                    })
                except:
                    pass

            # IO Counters
            io_counters = psutil.disk_io_counters()
            io_read = io_counters.read_count if io_counters else 0
            io_write = io_counters.write_count if io_counters else 0

            return {
                "disks": disks,
                "io_read": io_read,
                "io_write": io_write
            }
        except Exception as e:
            self.logger.log_message(f"Error getting filesystem info: {str(e)}")
            return None

    def get_services_info(self):
        """
        Retrieve system services information

        Returns:
            dict: Services information or None in case of error
        """
        try:
            services = []
            critical_services = []

            # List of typical critical services
            critical_service_names = [
                "sshd", "httpd", "apache2", "nginx", "mysql", "mariadb",
                "postgresql", "mongodb", "redis", "memcached", "docker", "containerd",
                "firewalld", "ufw", "ntpd", "systemd", "networkmanager", "cron"
            ]

            # Method for Linux (systemd)
            if platform.system() == "Linux":
                try:
                    output = subprocess.check_output(["systemctl", "list-units", "--type=service", "--state=running"]).decode()
                    service_count = 0

                    for line in output.split('\n'):
                        if '.service' in line and 'running' in line:
                            service_count += 1
                            service_name = line.split('.service')[0].strip()
                            services.append(service_name)

                            # Check if it's a critical service
                            for critical in critical_service_names:
                                if critical in service_name.lower():
                                    critical_services.append(service_name)
                                    break
                except:
                    # Alternative for non-systemd Linux
                    try:
                        output = subprocess.check_output(["service", "--status-all"]).decode()
                        for line in output.split('\n'):
                            if '[ + ]' in line:  # Active service
                                service_count += 1
                                service_name = line.split('[ + ]')[1].strip()
                                services.append(service_name)

                                # Check if it's a critical service
                                for critical in critical_service_names:
                                    if critical in service_name.lower():
                                        critical_services.append(service_name)
                                        break
                    except:
                        pass

            # Method for Windows
            elif platform.system() == "Windows":
                try:
                    output = subprocess.check_output(["net", "start"]).decode()
                    services = []
                    for line in output.split('\n'):
                        line = line.strip()
                        if line and not line.startswith('The following') and not line.startswith('The command'):
                            services.append(line)

                            # Check critical Windows services
                            windows_critical = ["Windows Firewall", "Windows Defender", "Windows Update",
                                               "SQL Server", "IIS", "DHCP", "DNS", "Print Spooler",
                                               "Remote Desktop", "Windows Time"]
                            for critical in windows_critical:
                                if critical.lower() in line.lower():
                                    critical_services.append(line)
                                    break
                except:
                    pass

            # If no info was obtained, try with psutil
            if not services:
                for proc in psutil.process_iter(['pid', 'name']):
                    for critical in critical_service_names:
                        if critical in proc.info['name'].lower():
                            critical_services.append(proc.info['name'])
                            break

            return {
                "running_count": len(services),
                "services": services,
                "critical": list(set(critical_services))  # Remove duplicates
            }
        except Exception as e:
            self.logger.log_message(f"Error getting services info: {str(e)}")
            return None
