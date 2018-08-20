

events {
worker_connections  10024;
}
http{
	proxy_redirect off;
	proxy_set_header Host $host;
	proxy_set_header Accept "*/*";
	proxy_set_header  X-Real-IP  $remote_addr;
	proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
	proxy_next_upstream http_404 http_502 http_504 error timeout invalid_header;
	proxy_set_header HTTP_CIP $remote_addr;
	proxy_set_header CIP $remote_addr;
	client_max_body_size    20m;
	client_body_buffer_size 256k;
	proxy_connect_timeout   10;
	proxy_send_timeout      30;
	proxy_read_timeout      30;
	proxy_buffer_size       256k;
	proxy_buffers           4 256k;
	proxy_busy_buffers_size 256k;
	proxy_temp_file_write_size 256k;
    server_names_hash_max_size 512;
    server_names_hash_bucket_size 128;
    log_format main '$remote_addr - $remote_user [$time_local] $request '
                '"$status" $body_bytes_sent "$http_referer" '
                '"$http_user_agent" "$http_x_forwarded_for" "$host" "$upstream_addr" $http_host';
    underscores_in_headers on;
    access_log  /data/kong/nginx/access.log  main ;

{{ range tree "uc/openapi/config/domain/"}}


						server{
							listen 80;
							charset utf-8;
							server_name {{ .Key }};

							{{ with $d := .Value| parseJSON }}
							location / {
											        proxy_redirect off;
											        proxy_set_header X-Real-IP $remote_addr;
											        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for; 
											        proxy_pass {{ $d.domain }};
							}	
						}

						{{ end }}
{{ end }}


}
