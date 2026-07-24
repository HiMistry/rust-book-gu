## Working with Environment Variables

આપણે `minigrep` બાઈનરીમાં એક વધારાની વિશેષતા ઉમેરીને તેને વધુ સારી બનાવીશું: કેસ-સેન્સિટિવ ન હોય તેવી શોધ માટેનો વિકલ્પ, જે user એક પર્યાવરણ variable સેટ કરી શકે છે. આપણે આ વિશેષતાને કમાન્ડ લાઇન વિકલ્પ બનાવી શકતા હતા અને દરેક વખતે જ્યારે તેઓ તેનો ઉપયોગ કરવા માંગતા હોય ત્યારે તેને દાખલ કરવાની જરૂર પડે તેમ કરી શકતા હતા, પરંતુ તેના બદલે તેને પર્યાવરણ variable બનાવવાથી, આપણે આપણા userઓને તે એકવાર પર્યાવરણ variable સેટ કરવાની અને તે ટર્મિનલ સત્રમાં તેમની બધી શોધ કેસ-સેન્સિટિવ ન હોય તેવી કરવાની મંજૂરી આપીએ છીએ.

<!-- Old headings. Do not remove or links may break. -->
### Writing a Failing Test for Case-Insensitive Search

અમે સૌપ્રથમ `minigrep` લાયબ્રેરીમાં એક નવું `search_case_insensitive` વિધેય ઉમેરીશું જે પર્યાવરણ variable (environment variable) ધરાવતું હોય ત્યારે બોલાશે. અમે TDD પ્રક્રિયાને અનુસરતા રહીશું, તેથી પ્રથમ પગલું ફરીથી નિષ્ફળ પરીક્ષણ લખવાનું છે. અમે નવા `search_case_insensitive` વિધેય માટે એક નવું પરીક્ષણ ઉમેરીશું અને અમારા જૂના પરીક્ષણને `case_sensitive` નામ આપીશું જેથી બે પરીક્ષણો વચ્ચેનો તફાવત સ્પષ્ટ થાય, જે યાદી 12-20 માં દર્શાવેલ છે.

<Listing number="12-20" file-name="src/lib.rs" caption="Adding a new failing test for the case-insensitive function we’re about to add">
```rust
{{#rustdoc_include ../listings/ch12-an-io-project/listing-12-20/src/lib.rs:here}}
```
</Listing>
અમે જૂના પરીક્ષણના `contents` માં ફેરફાર કર્યો છે. અમે એક નવી રેખા ઉમેરી છે જેમાં લખાણ `"Duct tape."` છે, જે મોટા અક્ષર D નો ઉપયોગ કરે છે જે કેસ-સંવેદનશીલ રીતે શોધ કરતી વખતે ક્વેરી `"duct"` સાથે મેળ ખાવું જોઈએ નહીં. આ રીતે જૂના પરીક્ષણને બદલવાથી એ સુનિશ્ચિત કરવામાં મદદ મળે છે કે અમે આકસ્મિક રીતે કેસ-સંવેદનશીલ શોધ કાર્યક્ષમતાને તોડી નાખીએ નહીં જે અમે પહેલાથી જ અમલમાં મૂકી છે. આ પરીક્ષણ હવે પાસ થવું જોઈએ અને જેમ જેમ

અમે કેસ-અસંવેદનશીલ શોધ પર કામ કરીશું તેમ તેમ તે ચાલુ રહેવું જોઈએ. કેસ-અસંવેદનશીલ શોધ માટેનું નવું પરીક્ષણ ક્વેરી તરીકે `"rUsT"` નો ઉપયોગ કરે છે. `search_case_insensitive` ફંક્શનમાં અમે ઉમેરવા જઈ રહ્યા છીએ, ત્યાં ક્વેરી `"rUsT"` મોટા અક્ષર R સાથેની રેખા `"Rust:"` અને `"Trust me."` બંને સાથે મેળ ખાય છે, ભલે તે ક્વેરી કરતાં અલગ કેસિંગ ધરાવતા હોય. આ આપણો નિષ્ફળ પરીક્ષણ છે, અને તે કમ્પાઇલ કરવામાં નિષ્ફળ જશે કારણ કે અમે હજી સુધી `search_case_insensitive` ફંક્શનને વ્યાખ્યાયિત કર્યું નથી. Listing 12-16 માં `search` ફંક્શન માટે કર્યા મુજબ હંમેશા ખાલી વેક્ટર પરત કરતા હાડપિંજર અમલીકરણ ઉમેરવા માટે નિઃસંકોચ રહો, જેથી પરીક્ષણ કમ્પાઇલ થાય અને નિષ્ફળ જાય.

### Implementing the `search_case_insensitive` Function

`search_case_insensitive` કાર્ય, યાદી 12-21 માં દર્શાવેલ છે, તે `search` કાર્ય જેવું જ લગભગ હશે. એકમાત્ર તફાવત એ છે કે અમે `query` અને દરેક `line` ને નાના અક્ષરમાં ફેરવીશું જેથી ઇનપુટ Argumentો (arguments) કયા પણ કેસમાં હોય, તેઓ તપાસ કરતી વખતે સમાન કેસમાં હોય.

<Listing number="12-21" file-name="src/lib.rs" caption="Defining the `search_case_insensitive` function to lowercase the query and the line before comparing them">
```rust
{{#rustdoc_include ../listings/ch12-an-io-project/listing-12-21/src/lib.rs:here}}
```
</Listing>
સૌ પ્રથમ, અમે `query` સ્ટ્રિંગને નાના અક્ષરોમાં ફેરવીએ છીએ અને તેને એક નવા variable (variable) માં સંગ્રહિત કરીએ છીએ, જેનું નામ પહેલાંના `query` ને છાયા પાડે છે. ક્વેરી પર `to_lowercase` બોલાવવું જરૂરી છે જેથી userની ક્વેરી `"rust"` , `"RUST"` , `"Rust"` અથવા `"rUsT"` હોય તો પણ, અમે ક્વેરીને જાણે તે `"rust"` હોય તેમ ગણીશું અને કેસ પ્રત્યે સંવેદનશીલ નહીં રહીએ. જ્યારે `to_lowercase` મૂળભૂત યુનિકોડ (Unicode) ને હેન્ડલ કરશે, ત્યારે તે 100 ટકા સચોટ રહેશે નહીં. જો અમે વાસ્તવિક એપ્લિકેશન લખતા હોત, તો અહીં થોડું વધારે કામ કરવું જોઈતું હતું, પરંતુ આ વિભાગ પર્યાવરણ variables (environment variables) વિશે છે, યુનિકોડ વિશે નહીં, તેથી અમે તેને ત્યાં જ છોડી દઈએ છીએ.

નોંધ હવે `query` એ સ્ટ્રિંગ સ્લાઇસને બદલે `String` છે, કારણ કે `to_lowercase` કૉલ કરવાથી નવું ડેટા ઉત્પન્ન થાય છે, હાલના ડેટાનો સંદર્ભ લેતો નથી. ઉદાહરણ તરીકે, જો `query` `"rUsT"` હોય, તો તે સ્ટ્રિંગ સ્લાઇસમાં નાના અક્ષર `u` કે `t` હોતું નથી, તેથી આપણે `"rust"` ધરાવતું નવું `String` ફાળવવું પડે છે. હવે જ્યારે આપણે `contains` પદ્ધતિને `query` Argument તરીકે પસાર કરીએ છીએ, ત્યારે આપણે એમ્પરસેન્ડ ઉમેરવાની જરૂર છે, કારણ કે `contains` ના હસ્તાક્ષર સ્ટ્રિંગ સ્લાઇસ લેવા માટે વ્યાખ્યાયિત કરવામાં આવ્યા છે.

આગળ, આપણે દરેક `line` પર `to_lowercase` ને બોલાવીએ છીએ જેથી બધા અક્ષરો નાના થઈ જાય. હવે કે જ્યારે આપણે `line` અને `query` બંનેને નાના અક્ષરમાં ફેરવી લીધા છે, ત્યારે આપણે કેસ ગમે તે હોય તો પણ મેળ ખાતી વસ્તુઓ શોધી શકીશું.

ચાલો જોઈએ કે આ અમલીકરણ પરીક્ષણો પાસ કરે છે કે નહીં:

```console
{{#include ../listings/ch12-an-io-project/listing-12-21/output.txt}}
```
ખૂબ સારું! તેઓ સફળ થયા. હવે આપણે નવા `search_case_insensitive` વિધેયને `run` વિધેયમાંથી બોલાવીશું. પ્રથમ, આપણે કેસ-સંવેદનશીલ અને કેસ-અસંવેદનશીલ શોધ વચ્ચે સ્વિચ કરવા માટે `Config` રચનામાં એક રૂપરેખાંકન વિકલ્પ ઉમેરીશું. આ ક્ષેત્ર ઉમેરવાથી કમ્પાઇલરની ભૂલો થશે કારણ કે આપણે હજી સુધી આ ક્ષેત્રને શરૂ કરી

રહ્યા નથી: Filename: src/main.rs

```rust
{{#rustdoc_include ../listings/ch12-an-io-project/listing-12-22/src/main.rs:here}}
```
અમે `ignore_case` ક્ષેત્ર ઉમેર્યું છે જે એક બુલિયન મૂલ્ય ધરાવે છે. હવે, આપણે `run` વિધેયને `ignore_case` ક્ષેત્રના મૂલ્યની ચકાસણી કરવા અને તેના આધારે નક્કી કરવા માટે જરૂરી છે કે `search` વિધેય અથવા `search_case_insensitive` વિધેયને બોલાવવું, જે યાદી 12-22 માં દર્શાવેલ છે. આ હજી સુધી કમ્પાઇલ થશે નહીં.

<Listing number="12-22" file-name="src/main.rs" caption="Calling either `search` or `search_case_insensitive` based on the value in `config.ignore_case`">
```rust
{{#rustdoc_include ../listings/ch12-an-io-project/listing-12-22/src/main.rs:there}}
```
</Listing>
અંતે, આપણે પર્યાવરણ variable (environment variable) માટે તપાસ કરવી જરૂરી છે. પર્યાવરણ variables સાથે કાર્ય કરવાના વિધેયો પ્રમાણિત પુસ્તકાલય (standard library) માં `env` મોડ્યુલમાં છે, જે src/main.rs ના પ્રારંભિક ભાગમાં પહેલાથી જ ઉપલબ્ધ છે. આપણે `var` વિધેયનો ઉપયોગ `env` મોડ્યુલમાંથી કરીશું, જેથી ચકાસી શકાય કે `IGNORE_CASE` નામનાં પર્યાવરણ variable માટે કોઈ મૂલ્ય સેટ થયું છે કે નહીં, જે યાદી 12-23 માં દર્શાવેલ છે.

<Listing number="12-23" file-name="src/main.rs" caption="Checking for any value in an environment variable named `IGNORE_CASE`">
```rust
{{#rustdoc_include ../listings/ch12-an-io-project/listing-12-23/src/main.rs:here}}
```
</Listing>
અહીં, આપણે એક નવું variable, `ignore_case`, બનાવીએ છીએ. તેની કિંમત સેટ કરવા માટે, આપણે `env::var` વિધેયને બોલાવીએ છીએ અને તેને `IGNORE_CASE` પર્યાવરણ ચલનું નામ પસાર કરીએ છીએ. `env::var` વિધેય એક `Result` આપે છે જે સફળ `Ok` પ્રકાર હશે જેમાં પર્યાવરણ variable's કિંમત હોય જો પર્યાવરણ variable કોઈ પણ મૂલ્ય પર સેટ કરેલો હોય. જો પર્યાવરણ variable સેટ ન હોય તો તે `Err` પ્રકાર આપશે.

આપણે `Result` પર `is_ok` પદ્ધતિનો ઉપયોગ કરીએ છીએ કે પર્યાવરણ variable સેટ છે કે નહીં તે તપાસવા માટે, જેનો અર્થ થાય છે કે પ્રોગ્રામને કેસ-સેન્સિટિવ શોધ કરવી જોઈએ. જો `IGNORE_CASE` પર્યાવરણ variable કોઈ પણ મૂલ્ય પર સેટ ન હોય, તો `is_ok` `false` આપશે અને પ્રોગ્રામ કેસ-સેન્સિટિવ શોધ કરશે. આપણે પર્યાવરણ variable's કિંમતની ચિંતા કરતા નથી, માત્ર તે સેટ છે કે અનસેટ છે તે તપાસીએ છીએ, તેથી આપણે `is_ok` તપાસી રહ્યા છીએ, `unwrap`, `expect`, અથવા `Result` પરની અન્ય પદ્ધતિઓનો ઉપયોગ કરવાને બદલે જે આપણે અત્યાર સુધી જોયા છે.

આપણે મૂલ્ય `ignore_case` variable `Config` ઉદાહરણમાં મોકલીએ છીએ જેથી `run` વિધેય તે મૂલ્ય વાંચી શકે અને નક્કી કરી શકે કે `search_case_insensitive` અથવા `search` ને બોલાવવું, જે રીતે અમે લિસ્ટિંગ 12-22 માં અમલમાં મુક્યું હતું.

ચાલો પ્રયત્ન કરીએ! પ્રથમ, આપણે પર્યાવરણ variable સેટ કર્યા વિના અને `to` ક્વેરી સાથે આપણું કાર્યક્રમ ચલાવીશું, જે કોઈપણ લાઇન સાથે મેળ ખાવું જોઈએ જેમાં બધા નાના અક્ષરોમાં શબ્દ to હોય.

```console
{{#include ../listings/ch12-an-io-project/listing-12-23/output.txt}}
```
દેખાય છે કે તે હજી કાર્યરત છે! હવે ચાલો પ્રોગ્રામને `IGNORE_CASE` ને `1` પર સેટ કરીને ચલાવીએ, પરંતુ એ જ પ્રશ્ન `to` સાથે:

```console
$ IGNORE_CASE=1 cargo run -- to poem.txt
```
જો તમે PowerShell વાપરી રહ્યા છો, તો તમારે પર્યાવરણ variable સેટ કરવું પડશે અને કાર્યક્રમને અલગ આદેશો તરીકે ચલાવવો પડશે:

```console
PS> $Env:IGNORE_CASE=1; cargo run -- to poem.txt
```
આથી `IGNORE_CASE` તમારા શેલ સત્રના બાકીના સમય માટે જળવાઈ રહેશે. તેને `Remove-Item` કમાન્ડલેટ વડે દૂર કરી શકાય છે:

```console
PS> Remove-Item Env:IGNORE_CASE
```
આપણે એવાં લીટીઓ મેળવવી જોઈએ જેમાં કે જે મોટા અક્ષરો ધરાવતાં હોઈ શકે.

<!-- manual-regeneration
cd listings/ch12-an-io-project/listing-12-23
IGNORE_CASE=1 cargo run -- to poem.txt
can't extract because of the environment variable
-->
```console
Are you nobody, too?
How dreary to be somebody!
To tell your name the livelong day
To an admiring bog!
```
ઉત્તમ, આપણને લાઈનો પણ મળી છે ! આપણો `minigrep` પ્રોગ્રામ હવે પર્યાવરણ variable દ્વારા નિયંત્રિત કેસ-સેન્સિટિવ શોધ કરી શકે છે. હવે તમે જાણો છો કે આદેશ વાક્ય Argumentો અથવા પર્યાવરણ variables બંનેનો ઉપયોગ કરીને સેટ કરેલા વિકલ્પોનું સંચાલન કેવી રીતે કરવું.

કેટલાક પ્રોગ્રામ્સ એક જ રૂપરેખાંકન માટે Argumentો અને પર્યાવરણ variable મંજૂરી આપે છે. તેવા કિસ્સાઓમાં, પ્રોગ્રામ નક્કી કરે છે કે એક અથવા બીજાની પ્રાથમિકતા લેવી. તમારા પોતાના માટે અન્ય કસરત તરીકે, આદેશ વાક્ય Argument અથવા પર્યાવરણ variable દ્વારા કેસ સંવેદનશીલતાને નિયંત્રિત કરવાનો પ્રયાસ કરો. નક્કી કરો કે જો પ્રોગ્રામને એક કેસ-સેન્સિટિવ અને એકને અવગણવા માટે સેટ કરવામાં આવે તો કમાન્ડ લાઇન Argument અથવા પર્યાવરણ variable's પ્રાથમિકતા હોવી જોઈએ.

`std::env` મોડ્યુલમાં પર્યાવરણ variable (environment variables) સાથે કામ કરવા માટે ઘણા વધારે ઉપયોગી લક્ષણો છે: ઉપલબ્ધ શું છે તે જોવા માટે તેના દસ્તાવેજીકરણ તપાસો.

