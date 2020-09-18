# ha-custom-component-ituran
Ituran component for Home Assistant


usage:

first, download the files and put them in the right directories like in this repo.
then, you need to install xmltodict 
```
pip3 install xmltodict
```

in your configuration.yaml, add:

```

ituran:
  bmw760li:
    name: BMW
    username: 'myIturanUsername'
    password: 'myIturanPassword'
    update_interval: 180
```


and for Lovelace UI, in ui-lovelace.yaml:

```
resources:
  - url: /local/content-card-ituran.js
    type: module
```

and add your card:
```
- icon: mdi:car
  id: cars
  panel: false
  cards:
  - type: "custom:content-card-ituran"
    entity: ituran.bmw
 ```



and thats it. you have your ituran component ready

![Ituran](https://preview.ibb.co/chwMxS/Screen_Shot_2018_04_20_at_16_53_21.png)
