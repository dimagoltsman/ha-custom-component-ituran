# ha-custom-component-ituran
Ituran component for Home Assistant


usage:

first, download the files and put them in the right directories like in this repo.

in your configuration.yaml, add:

```
frontend:
  extra_html_url:
    - /local/custom_ui/state-card-ituran.html


ituran:
  bmw760li:
    name: BMW
    username: 'myIturanUsername'
    password: 'myIturanPassword'
```

and thats it. you have your ituran component ready

![Ituran](https://preview.ibb.co/chwMxS/Screen_Shot_2018_04_20_at_16_53_21.png)
