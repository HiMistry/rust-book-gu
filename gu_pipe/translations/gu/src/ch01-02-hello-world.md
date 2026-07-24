## Hello, World!

હવે તમે Rust સ્થાપિત કરી લીધું છે, તો હવે પહેલું Rust કાર્યક્રમ લખવાનો સમય આવી ગયો છે. નવી ભાષા શીખતી વખતે કોઈ નાનું કાર્યક્રમ છાપવો એ પરંપરા છે જે `Hello, world!` લખાણ સ્ક્રીન પર દર્શાવે છે, તેથી આપણે પણ તે જ કરીશું!

નોંધ: આ પુસ્તક કમાન્ડ લાઇનથી થોડી પૃથ્થઈ પરિચય હોવાનું માને છે. Rust તમારા સંપાદન કે સાધન અથવા તમારો કોડ ક્યાં રહે છે તેના વિશે કોઈ ચોક્કસ માંગણી કરતું નથી, તેથી જો તમે કમાન્ડ લાઇનને બદલે IDE વાપરવાનું પસંદ કરો છો, તો તમારા મનપસંદ IDE નો ઉપયોગ કરી શકો છો. ઘણા IDEs હવે Rust માટે થોડી ઘણી મદદ પૂરી પાડે છે; વિગતો માટે IDE ના દસ્તાવેજ તપાસો. Rust ટીમ `rust-analyzer` દ્વારા મહાન IDE મદદ આપવા પર ધ્યાન કેન્દ્રિત કરી રહી છે. વધુ માહિતી માટે [Appendix D][devtools] જુઓ.

<!-- Old headings. Do not remove or links may break. -->
### Project Directory Setup

તમે એક ડિરેક્ટરી બનાવીને શરૂઆત કરશો જ્યાં તમે તમારો Rust કોડ સંગ્રહિત કરશો. Rust ને એનાથી કોઈ ફરક પડતો નથી કે તમારો કોડ ક્યાં રહે છે, પરંતુ આ પુસ્તકમાં આપેલાં વ્યાયમો અને પ્રોજેક્ટ્સ માટે, અમે તમારા હોમ ડિરેક્ટરીમાં એક `projects` ડિરેક્ટરી બનાવવાની અને બધાં પ્રોજેક્ટ્સ ત્યાં રાખવાની ભલામણ કરીએ છીએ.

એક ટર્મિનલ ખોલો અને `projects` ડિરેક્ટરી અને "Hello, world!" પ્રોજેક્ટ માટેની ડિરેક્ટરી બનાવવા માટે નીચેના આદેશો દાખલ કરો.

Linux, macOS, અને Windows પર PowerShell માટે, આ દાખલ કરો:

```console
$ mkdir ~/projects
$ cd ~/projects
$ mkdir hello_world
$ cd hello_world
```
વિન્ડોઝ CMD માટે, આ દાખલ કરો:

```cmd
> mkdir "%USERPROFILE%\projects"
> cd /d "%USERPROFILE%\projects"
> mkdir hello_world
> cd hello_world
```
<!-- Old headings. Do not remove or links may break. -->
### Rust Program Basics

ત્યારબાદ, એક નવી સ્ત્રોત ફાઈલ બનાવો અને તેનું નામ main.rs રાખો. Rust ફાઈલો હંમેશાં .rs એક્સટેન્શન સાથે સમાપ્ત થાય છે. જો તમે તમારી ફાઇલનામમાં એક કરતાં વધુ શબ્દોનો ઉપયોગ કરી રહ્યા છો, તો સંમેલન મુજબ તેમને અન્ડરસ્કોરથી અલગ કરો. ઉદાહરણ તરીકે, hello_world.rs નો ઉપયોગ કરોhelloworld.rs ને બદલે.

હવે બનાવેલી main.rs ફાઈલ ખોલો અને Listing 1-1 માં આપેલ કોડ દાખલ કરો.

<Listing number="1-1" file-name="main.rs" caption="A program that prints `Hello, world!`">
```rust
fn main() {
    println!("Hello, world!");
}
```
</Listing>
ફાઈલ સાચવો અને તમારા ટર્મિનલ વિન્ડોમાં પાછા જાઓ ~/projects/hello_world ડિરેક્ટરીમાં. લિનક્સ અથવા મૅકઓએસ પર, ફાઈલને કમ્પાઇલ કરવા અને ચલાવવા માટે નીચેના આદેશો દાખલ કરો:

```console
$ rustc main.rs
$ ./main
Hello, world!
```
વિન્ડોઝ પર, આદેશ `.\main` દાખલ કરો, `./main` ને બદલે:

```powershell
> rustc main.rs
> .\main
Hello, world!
```
તમારા ઓપરેટિંગ સિસ્ટમ કેવું હોય વાંધો નહિ, `Hello, world!` એ આઉટપુટ ટર્મિનલ પર દેખાવા જોઈએ. જો તમને આ આઉટપુટ ના દેખાય, તો સહાય મેળવવા માટે ઇન્સ્ટોલેશન વિભાગના [“Troubleshooting”][troubleshooting] ભાગમાં પાછા જાઓ. If `Hello, world!` did print,

જો `Hello, world!` છપાયું હોય, તો અભિનંદન! તમે સત્તાવાર રીતે એક Rust કાર્યક્રમ લખ્યો છે. એ તમને એક Rust પ્રોગ્રામર બનાવે છે—સ્વાગત છે!

<!-- Old headings. Do not remove or links may break. -->
### The Anatomy of a Rust Program

ચાલો આ "Hello, world!" કાર્યક્રમને વિગતવાર જોઈએ. અહીં પ્રથમ ભાગ છે:

```rust
fn main() {

}
```
These lines define a function named `main`. The `main` function is special: It is always the first code that runs in every executable Rust program. Here, the first line declares a function named `main` that has no parameters and returns nothing. If there were parameters, they would go inside the parentheses (`()`).

The function body is wrapped in `{}`. Rust requires curly brackets around all function bodies. It’s good style to place the opening curly bracket on the same line as the function declaration, adding one space in between.

નોંધ: જો તમે બધા Rust પ્રોજેક્ટ્સમાં એકસમાન શૈલી જાળવવા માંગતા હો, તો તમે `rustfmt` નામના આપોઆપ ફોર્મેટર સાધનનો ઉપયોગ કરી શકો છો જે તમારા કોડને ચોક્કસ શૈલીમાં ફોર્મેટ કરે છે ( `rustfmt` વિશે વધુ માહિતી [Appendix D][devtools] માં મળશે). Rust ટીમ આ સાધનને સ્ટાન્ડર્ડ Rust વિતરણ સાથે સામેલ કર્યું છે, જેમ કે `rustc`, તેથી તે પહેલાથી જ તમારા કમ્પ્યુટર પર ઇન્સ્ટોલ થયેલ હોવું જોઈએ!

`main` ફંક્શનનો મુખ્ય ભાગ નીચેના કોડ ધરાવે છે:

```rust
println!("Hello, world!");
```
આ લીટી આ નાનકડા કાર્યક્રમમાં તમામ કાર્ય કરે છે: તે સ્ક્રીન પર લખાણ છાપે છે. અહીં ત્રણ મહત્વપૂર્ણ વિગતો ધ્યાન રાખવા જેવી છે.

પ્રથમ, `println!` એક Rust મેક્રોને બોલાવે છે. જો તેના બદલે કોઈ ફંક્શન બોલાવવામાં આવ્યું હોત, તો તેને `println` ( `!` વગર) તરીકે દાખલ કરવામાં આવતું હોત. Rust મેક્રો એ કોડ લખવાનો એક માર્ગ છે જે Rust વાક્યરચનાને વિસ્તારવા માટે કોડ જનરેટ કરે છે, અને આપણે તેના વિશે પ્રકરણ 20 માં વધુ વિગતવાર ચર્ચા કરીશું. અત્યારે, તમારે માત્ર એટલું જ જાણવાની જરૂર છે કે `!` નો ઉપયોગ કરવો એ સામાન્ય ફંક્શનને બદલે મેક્રોને બોલાવવા સમાન છે અને મેક્રો હંમેશાં ફંક્શન જેવા નિયમોનું પાલન કરતા નથી.

બીજું, તમે `"Hello, world!"` સ્ટ્રિંગ જુઓ છો. અમે આ સ્ટ્રિંગને `println!` ને Argument તરીકે પસાર કરીએ છીએ, અને સ્ટ્રિંગ સ્ક્રીન પર છપાય છે. ત્રીજું, આપણે

લીટીને સેમિકોલન ( `;` ) સાથે સમાપ્ત કરીએ છીએ, જે દર્શાવે છે કે આ અભિવ્યક્તિ પૂર્ણ થઈ ગઈ છે, અને આગામી શરૂ થવા માટે તૈયાર છે. મોટાભાગની Rust કોડની લીટીઓ સેમિકોલનથી અંતિમ થાય છે.

<!-- Old headings. Do not remove or links may break. -->
### Compilation and Execution

તમે હમણાં જ એક નવું બનાવેલું કાર્યક્રમ ચલાવ્યો છે, તો ચાલો આ પ્રક્રિયાના દરેક તબક્કાની તપાસ કરીએ.

Rust કાર્યક્રમ ચલાવતા પહેલાં, તમારે તેને Rust કંપક (compiler) દ્વારા કમ્પાઇલ કરવું આવશ્યક છે, જેમાં `rustc` આદેશ દાખલ કરીને અને તમારા સ્ત્રોત ફાઈલનું નામ પસાર કરીને, જેમ કે:

```console
$ rustc main.rs
```
જો તમને C અથવા C++ નો અનુભવ હોય, તો તમે નોંધશો કે આ `gcc` અથવા `clang` જેવું જ છે. સફળતાપૂર્વક કમ્પાઈલ કર્યા પછી, Rust એક બાઈનરી એક્ઝિક્યુટેબલ ફાઈલ

ઉત્પન્ન કરે છે. Linux, macOS અને Windows પર PowerShell માં, તમે `ls` આદેશ તમારા શેલમાં દાખલ કરીને એક્ઝિક્યુટેબલ જોઈ શકો છો:

```console
$ ls
main  main.rs
```
Linux અને macOS પર, તમે બે ફાઈલો જોશો. Windows પર PowerShell સાથે, તમને એ જ ત્રણ ફાઈલો દેખાશે જે CMD વાપરતી વખતે દેખાત. Windows પર CMD સાથે, તમારે નીચે મુજબ કરવું જોઈએ:

```cmd
> dir /B %= the /B option says to only show the file names =%
main.exe
main.pdb
main.rs
```
આ દર્શાવે છે કે સ્ત્રોત કોડ ફાઈલ કઈ સાથે .rs એક્સ્ટેંશન ધરાવે છે, એક્ઝિક્યુટેબલ ફાઈલ (Windows પર main.exe, પરંતુ અન્ય તમામ પ્લેટફોર્મ પર main), અને, Windows વાપરતી વખતે, એક ફાઈલ જેમાં ડીબગીંગ માહિતી હોય જે .pdb એક્સ્ટેંશન સાથે હોય. અહીંથી, તમે main અથવા main.exe ફાઈલ ચલાવો છો, આ રીતે:

```console
$ ./main # or .\main on Windows
```
જો તમારું main.rs ફાઈલ "હેલો, વર્લ્ડ!" પ્રોગ્રામ છે, તો આ લીટી તમારા ટર્મિનલમાં `Hello, world!` છાપે છે.

જો તમે ડાયનેમિક ભાષાથી વધુ પરિચિત છો, જેમ કે રૂબી, પાયથોન અથવા JavaScript, તો તમને પ્રોગ્રામને અલગ તબક્કામાં કમ્પાઇલ કરવું અને ચલાવવું સામાન્ય ન લાગી શકે. Rust એ એક અગાઉથી કમ્પાઈલ કરેલી ભાષા છે, જેનો અર્થ થાય છે કે તમે પ્રોગ્રામને કમ્પાઇલ કરી શકો છો અને તેને કોઈ બીજાને આપી શકો છો, અને તેઓ Rust ઇન્સ્ટોલ કર્યા વિના પણ ચલાવી શકે છે. જો તમે કોઈને .rb , .py , અથવા .js ફાઈલ આપો છો, તો તેમને રૂબી, પાયથોન અથવા JavaScript અમલીકરણ ઇન્સ્ટોલ કરવું પડશે (ક્રમશઃ). પરંતુ તે ભાષાઓમાં, તમારે તમારા પ્રોગ્રામને કમ્પાઇલ કરવા અને ચલાવવા માટે માત્ર એક જ આદેશની જરૂર પડે છે. ભાષા ડિઝાઇન હંમેશાં આપ-લેનું પરિણામ હોય છે.

`rustc` વડે માત્ર કમ્પાઇલ કરવું સરળ પ્રોગ્રામ માટે ઠીક છે, પરંતુ જેમ જેમ તમારી યોજના વિશાળ બનશે, તેમ તમને બધા વિકલ્પોનું સંચાલન કરવું અને તમારા કોડને વહેંચવાનું સરળ બનાવવું જોઈશે. હવે પછી, અમે Cargo સાધનપરિચય કરાવશે, જે તમને વાસ્તવિક દુનિયાના Rust પ્રોગ્રામ લખવામાં મદદ કરશે.



[troubleshooting]: ch01-01-installation.html#troubleshooting
[devtools]: appendix-04-useful-development-tools.html
[ch20-macros]: ch20-05-macros.html
