

{{ $filtered :=  service "openapi-lan-kong|passing" }}
{{ if eq (len $filtered) 0 }}
	{{ range tree "uc/openapi/config/domain/"}}

	events {
    worker_connections  1024;
}

http{

						server{
							listen 80;
							charset utf-8;
							server_name {{ .Key }};
							{{ with $d := .Value| parseJSON }}
							location / {
											        proxy_redirect off;
											        proxy_set_header Host $host;
											        proxy_set_header X-Real-IP $remote_addr;
											        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for; 
											        proxy_pass {{ $d.domain }};
							}	
						}
	}
						{{ end }}
			{{ end }}
{{ else }}
    {{ range $service := $filtered }}
        range over available and non empty services
    {{ end }}
{{ end }}



