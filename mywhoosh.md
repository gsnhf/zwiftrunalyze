# MyWhoosh 

## Links 

- [CUrl to Code Converter](https://curlconverter.com/python/)  

## Requests Login

### Url

### CUrl
```
curl 'https://event.mywhoosh.com/api/auth/login' \
  -H 'authority: event.mywhoosh.com' \
  -H 'accept: application/json' \
  -H 'accept-language: de-DE,de;q=0.9,en-US;q=0.8,en;q=0.7,it;q=0.6' \
  -H 'content-type: application/json' \
  -H 'cookie: _fbp=fb.1.1708710018062.609185162; mywhooshweb_session=AjfyBtKSahDNZ2OnIFQr0FPbYUfj8n7QGv8j5kaM; twk_uuid_5f66f45ff0e7167d0011f3e0=%7B%22uuid%22%3A%221.SwoJog5v0TtLA7s2980UzdjRpg8Q0UYFzUNOBYC1HykBQjqSELHDWcMaXsV0F1Vtx1wkryX9PJy4i4u0gQAD6ladfdQ4ae378qfxMSk12NqoOJrh2R9RZ%22%2C%22version%22%3A3%2C%22domain%22%3A%22mywhoosh.com%22%2C%22ts%22%3A1708710023370%7D' \
  -H 'origin: https://event.mywhoosh.com' \
  -H 'referer: https://event.mywhoosh.com/auth/login' \
  -H 'sec-ch-ua: "Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122"' \
  -H 'sec-ch-ua-mobile: ?0' \
  -H 'sec-ch-ua-platform: "macOS"' \
  -H 'sec-fetch-dest: empty' \
  -H 'sec-fetch-mode: cors' \
  -H 'sec-fetch-site: same-origin' \
  -H 'user-agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36' \
  --data-raw '{"remember":false,"password":"MySecretPassword","email":"mysecret@mail.com"}'
```
.