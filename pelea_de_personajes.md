# Pelea de personajes

Usando la API https://www.superheroapi.com/ (probablemente quieras ver la fuente aquí: https://akabab.github.io/superhero-api/) simula un conjunto de peleas entre superhéroes y villanos. Puedes definir las condiciones de las peleas como desees, sólo recuerda especificarlo para que después pueda entender la lógica.

Para simular las batallas, debes crear dos equipos de 5 personajes de forma aleatoria utilizando la api, siguiendo las siguientes consideraciones:

- No pueden haber personajes repetidos (de la misma ID).
- A cada uno de los personajes, por cada uno de sus stats (intelligence, strength, speed, durability, power, combat) deberas asignarles una nueva variable de forma aleatoria llamada AS (Actual Stamina). Este valor debe tomar un valor del rango del 0 al 10.
- Los personajes pueden ser buenos o malos según el campo Alignment , la inclinación del equipo será el de la mayoría. Por ejemplo, si en el equipo hay 3 buenos y 2 malos, entonces el equipo es bueno.
- A cada personaje se le aplicará un bonus o una penalización según la naturaleza del personaje (bueno o malo ) versus la de su equipo que se llamará FB (Filiation Coefficient). Si su equipo es de la misma Alignment que el personaje, entonces es una bonificación, de lo contrario será una penalización. [1]
- Los personajes tendrán tres ataques que se basarán en sus stats [2]. La elección del ataque será aleatoria.

Con los datos anteriores, cada pelea la debes simular con sus stats reales, que se calculan con la fórmula a continuación:
`HP = math.floor((strength * 0.8 + durability * 0.7 + power) / 2 * (1 + AS / 10)) + 100`
`stats = math.floor(((2 * Base + AS) / 1.1) * FB)`

Pelea de personajes 1

* HP = Health Points o puntos de vida.  
[1] La forma de calcular el FB es la siguiente:
```
if Alignment_team == Alignment_character: 
	FB = 1 + random.randint(0, 9) 
else: 
	FB = (1 + random.randint(0, 9)) ** -1
```
[2] Para los ataques se tendrán tres tipos y el daño que ocasionarán será como dicta en cada caso:

Mental
- `mental = (intelligence * 0.7 + speed * 0.2 + combat * 0.1) * FB`

Strong
- `strong = (strength * 0.6 + power * 0.2 + combat * 0.2) * FB`
Fast
- `fast = (speed * 0.55 + durability * 0.25 + strength * 0.2) * FB`

El resultado de cada ataque se descuenta directamente en el HP del oponente. El primer personaje en llegar a 0 pierde la pelea y a la siguiente se le reinician los puntos HP.

El avance y el resultado de las batallas se debe imprimir en la consola.

El equipo vencedor de la batalla será quien tenga al último (o últimos) personajes en pie.

## Bonus

Esto es por si quieres añadir algo choro. En el caso de que se te haya hecho muy fácil esta prueba, puedes agregar la conexión a la API de algún proveedor de mail. Nosotros

Pelea de personajes 2

te recomendamos mailgun porque es gratis para hasta 5 direcciones de correo (puedes ocupar otra API si así deseas ).

El reto consiste en que la simulación reciba de input una dirección email y mande un resumen de todas las peleas, con el nombre de los combatientes de cada una y el vencedor. Finalmente en **negrita** tienes que poner al equipo vencedor.