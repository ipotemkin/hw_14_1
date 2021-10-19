NETFLIX DB API
===

A simple API application for querying a local Netflix database
---

Functions realized:
---

> Get films by title. Any part of a film title is valid, search case-insensitive. Return the first found
>> `GET /movie/title/?s=train`
> ```json
> [{
>  "country": "South Korea",
>  "description": "Keeping peace and safety in Train World is no easy task, but for five trains with the power to transform into robots, every crisis is an adventure!\n", 
>  "genre": "Kids' TV, Korean TV Shows", 
>  "release_year": 2018,
>  "title": "Robot Trains"
> }]
>```



> Get first 100 films by release years between year1 qnd year2
>> `GET /movie/year/year1/year2`
> ```json
> [{
>  "release_year": 2020, 
>  "title": "3%"
> },
> {
> "release_year": 2019,
> "title": "122"
> }]
>```

> Get films by category (children, family, adult)
>> `GET /category/children`
> ```json
> [{
>  "description": "When a grieving teen must work off her debt to a ranch, she cares for a wounded horse that teaches her more about healing than she expected.\n", 
>  "rating": "G",
>  "title": "A Champion Heart"
> }, 
> {
>  "description": "Shaun and the flock race to help an adorable alien find her way home after her ship crash-lands near Mossy Bottom Farm and sparks a UFO frenzy.\n",
>  "rating": "G",
>  "title": "A Shaun the Sheep Movie: Farmageddon"
> }]
>```

> Get films by genre
>> `GET /genre/thriller`
> ```json
> [{
>   "description": "A master thief who uses her skills for good, Carmen Sandiego travels the world foiling V.I.L.E.'s evil plans – with help from her savvy sidekicks.\n",
>   "title": "Carmen Sandiego"
> },
> {
>   "description": "As a grisly virus rampages a city, a lone man stays locked inside his apartment, digitally cut off from seeking help and desperate to find a way out.\n",
>   "title": "#Alive"
> }]
>```

> Get pairs (>2 times) to the two given actors
>> `GET /2actors/?actor1=Name Surname&actor2=Name Surname`
> 
>> `GET /2actors/?actor1=Rose McIver&actor2=Ben Lamb`
> ```json
> [
>   "Alice Krige",
>   "Honor Kneafsey"
> ]
>```

> Finds movies by type, year or genre
>> `GET /movie/?year=2020&type=Movie&genre=Thrillers`
> ```json
> [{
>   "description": "As a grisly virus rampages a city, a lone man stays locked inside his apartment, digitally cut off from seeking help and desperate to find a way out.\n",
>   "title": "#Alive"
> },
> {
>   "description": "When gentle, law-abiding Grace confesses to killing her new husband, her skeptical young lawyer sets out to uncover the truth. A film by Tyler Perry.\n",
>   "title": "A Fall from Grace"
> }]
>```
