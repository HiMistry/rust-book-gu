<!-- Old headings. Do not remove or links may break. -->
## A Closer Look at the Traits for Async

આ પ્રકરણમાં, અમે `Future`, `Stream`, અને `StreamExt` traits નો ઉપયોગ વિવિધ રીતે કર્યો છે. અત્યાર સુધી, અમે એમના કાર્ય કરવાની રીત અથવા એમના એકબીજા સાથે કેવી રીતે બંધાયેલા છે તે વિગતોમાં વધુ ઊંડા ઉતરવાનું ટાળ્યું છે, જે મોટાભાગના સમય માટે તમારા દૈનિક Rust કાર્ય માટે યોગ્ય છે. જો કે, કેટલીકવાર તમે એવી પરિસ્થિતિઓનો સામનો કરશો જ્યાં તમારે આ traits ની થોડી વધુ વિગતો સમજવાની જરૂર પડશે, સાથે સાથે `Pin` type અને `Unpin` trait પણ. આ વિભાગમાં, અમે માત્ર એટલા જ ઊંડા ઉતરશું જેથી તે દૃશ્યોમાં મદદ મળી શકે, હજુ પણ ખરેખર ગહન અભ્યાસ અન્ય documentation માટે છોડી દેવામાં આવશે.

<!-- Old headings. Do not remove or links may break. -->
### The `Future` Trait

ચાલો, સૌપ્રથમ જોઈએ કે `Future` લક્ષણ કેવી રીતે કાર્ય કરે છે. અહીં Rust દ્વારા તે વ્યાખ્યાયિત થયેલું છે:

```rust
```rust
use std::pin::Pin;
use std::task::{Context, Poll};

pub trait Future {
    type Output;

    fn poll(self: Pin<&mut Self>, cx: &mut Context<'_>) -> Poll<Self::Output>;
}
```
```
તે ટ્રેઇટ વ્યાખ્યામાં ઘણા નવા પ્રકારો

અને આપણે પહેલાં ન જોયેલા સિન્ટેક્સનો પણ સમાવેશ થાય છે, તેથી ચાલો વ્યાખ્યાને ભાગ-ભાગ કરીને સમજીએ. પ્રથમ, `Future` નું સંકળાયેલ પ્રકાર `Output` જણાવે છે કે ભવિષ્ય શું પરિણામ આપે છે. આ `Iterator` ટ્રેઇટ માટેના `Item` સંકળાયેલ પ્રકાર સાથે સમાન છે. બીજું, `Future` માં `poll` નામની પદ્ધતિ છે, જે તેના `self` પેરામીટર માટે એક વિશેષ `Pin` સંદર્ભ અને એક પરિવર્તનશીલ સંદર્ભ `Context` પ્રકાર માટે લે છે, અને `Poll<Self::Output>` આપે છે. આપણે થોડી વારમાં `Pin` અને `Context` વિશે વધુ વાત કરીશું. અત્યારે, ચાલો જોઈએ કે પદ્ધતિ શું પરિણામ આપે છે, જે `Poll` પ્રકાર છે:

```rust
```rust
pub enum Poll<T> {
    Ready(T),
    Pending,
}
```
```
આ `Poll` પ્રકાર `Option` જેવો જ છે. તેની એક વિવિધતામાં મૂલ્ય હોય છે, `Ready(T)`, અને બીજીમાં ન હોય છે, `Pending`. `Poll` નો અર્થ `Option` કરતા ઘણો અલગ છે! `Pending` વિવિધતા દર્શાવે છે કે ભવિષ્યને (future) હજી કાર્ય કરવાનું બાકી છે, તેથી કૉલરને પાછળથી ફરીથી તપાસવાની જરૂર પડશે. `Ready` વિવિધતા દર્શાવે છે કે `Future` એ તેનું કાર્ય પૂર્ણ કરી લીધું છે અને `T`

મૂલ્ય ઉપલબ્ધ છે. નોંધ: સીધા `poll` ને બોલાવવું કદાચિત જરૂરી નથી, પરંતુ જો તમારે તે કરવાની જરૂર હોય, તો યાદ રાખો કે મોટા ભાગના ભવિષ્ય માટે, કૉલરને `Ready` પરત થયા પછી `poll` ફરીથી બોલાવો જોઈએ નહીં. ઘણા ભવિષ્ય તૈયાર થયા પછી ગભરાટ (panic) કરી શકે છે. જે ભવિષ્યને ફરીથી પોલિંગ કરવું સલામત હોય તે તેમના દસ્તાવેજોમાં સ્પષ્ટપણે જણાવશે. આ વર્તન `Iterator::next` જેવું જ છે.

જ્યારે તમે `await` વાપરતા કોડ જુઓ છો, ત્યારે Rust તેને `poll` કૉલ કરતો કોડમાં રૂપાંતરિત કરે છે. જો તમે યાદ કરો Listing 17-4, જ્યાં આપણે એક URL માટે પૃષ્ઠનું શીર્ષક છપાવ્યું હતું જ્યારે તે ઉકેલાઈ ગયું, તો Rust તેને કંઈક એવું (જો કે બરાબર નહીં) માં ફેરવે છે:

```rust
```rust
match page_title(url).poll() {
    Ready(page_title) => match page_title {
        Some(title) => println!("The title for {url} was {title}"),
        None => println!("{url} had no title"),
    }
    Pending => {
        // But what goes here?
    }
}
```
```
ભવિષ્ય હજી `Pending` હોય તો શું કરવું જોઈએ? આપણને ફરીથી પ્રયત્ન કરવાની કોઈ રીત જોઈએ છે, અને ફરીથી, અને ફરીથી, જ્યાં સુધી ભવિષ્ય અંતિમ રીતે તૈયાર ન થઈ જાય. બીજા શબ્દોમાં કહીએ તો, આપણને એક લૂપ (loop) જોઈએ:

```rust
```rust
let mut page_title_fut = page_title(url);
loop {
    match page_title_fut.poll() {
        Ready(value) => match page_title {
            Some(title) => println!("The title for {url} was {title}"),
            None => println!("{url} had no title"),
        }
        Pending => {
            // continue
        }
    }
}
```
```
જો Rust એ બરાબર તે જ કોડમાં કમ્પાઇલ કરેલું હોત, તો દરેક `await` બ્લોકિંગ બની જાત—જે આપણે મેળવવા માંગતા હતા તેનાથી તદ્દન વિરુદ્ધ! તેના બદલે, Rust ખાતરી કરે છે કે લૂપ નિયંત્રણ કોઈ એવી વસ્તુને સોંપી શકે છે જે આ ફ્યુચર પરનું કાર્ય થોભાવે અને અન્ય ફ્યુચર્સ પર કામ કરી શકે અને પછી આને ફરીથી તપાસી શકે. આપણે જોયું છે તેમ, તે કંઈક એસિંક રનટાઇમ છે, અને આ શેડ્યૂલિંગ અને સંકલન કાર્ય તેની મુખ્ય જવાબદારીઓમાંનું એક છે.

“બે કાર્યો વચ્ચે સંદેશા દ્વારા ડેટા મોકલવો” વિભાગમાં, આપણે `rx.recv` ની રાહ જોવાની વાત કરી હતી. `recv` કૉલ એક ફ્યુચર આપે છે, અને તેના માટે `await` કરવાથી તેને પોલ કરવામાં આવે છે. અમે નોંધ્યું હતું કે રનટાઇમ ફ્યુચરને ત્યાં સુધી થોભાવશે જ્યાં સુધી તે `Some(message)` અથવા ચેનલ બંધ થાય ત્યારે `None` સાથે તૈયાર ન થઈ જાય. `Future` ટ્રેઇટની આપણી ઊંડી સમજણ સાથે, અને વિશેષ કરીને `Future::poll` સાથે, આપણે જોઈ શકીએ છીએ કે તે કેવી રીતે કાર્ય કરે છે. રનટાઇમ જાણે છે કે ફ્યુચર તૈયાર નથી જ્યારે તે `Poll::Pending` આપે છે. તેનાથી વિપરીત, રનટાઇમ જાણે છે કે ફ્યુચર તૈયાર છે અને `poll`  `Poll::Ready(Some(message))` અથવા `Poll::Ready(None)` આપતું હોય ત્યારે તેને આગળ વધારે છે.

આ પુસ્તકની કાર્યક્ષેત્ર બહારની બાબતો છે કે રનટાઇમ કેવી રીતે તે કરે છે, પરંતુ મહત્વનું એ સમજવાનું છે કે ફ્યુચર્સની મૂળભૂત પદ્ધતિઓ: એક રનટાઇમ પોતાની જવાબદારી હેઠળના દરેક ફ્યુચરને તપાસે છે, અને જ્યારે તે તૈયાર ન હોય ત્યારે તેને નિષ્ક્રિય કરી દે છે.

<!-- Old headings. Do not remove or links may break. -->
### The `Pin` Type and the `Unpin` Trait

પાછલા યાદી ૧૭-૧૩ માં, અમે ત્રણ futures ની રાહ જોવા માટે `trpl::join!` macro નો ઉપયોગ કર્યો હતો. જો કે, ઘણીવાર એવી કલેક્શન (collection) હોય છે, જેમ કે વેક્ટર (vector), જેમાં અમુક સંખ્યાના futures હોય છે જે રનટાઇમ (runtime) સુધી જાણીતા હોતા નથી. ચાલો યાદી ૧૭-૧૩ ને યાદી ૧૭-૨૩ માં બદલીએ, જે ત્રણ futures ને વેક્ટરમાં મૂકે છે અને `trpl::join_all` ફંક્શનને બોલાવે છે, જે હજી કમ્પાઇલ (compile) થશે નહીં.

<Listing number="17-23" caption="Awaiting futures in a collection"  file-name="src/main.rs">
```rust
```rust
{{#rustdoc_include ../listings/ch17-async-await/listing-17-23/src/main.rs:here}}
```
```
</Listing>
આપણે દરેક ભવિષ્યને `Box` માં મૂકીએ છીએ જેથી તે trait object બને, જેમ કે આપણે પ્રકરણ ૧૨ ના “Returning Errors from `run`” વિભાગમાં કર્યું હતું. (આપણે પ્રકરણ ૧૮ માં trait objects વિશે વિગતવાર વાત કરીશું.) trait objects નો ઉપયોગ કરવાથી, આપણે આ પ્રકારો દ્વારા ઉત્પાદિત અનામી ભવિષ્યને સમાન પ્રકાર તરીકે ગણી શકીએ છીએ, કારણ કે તે બધા `Future` trait ને અમલમાં મૂકે છે. This might be surprising.

આ આશ્ચર્યજનક હોઈ શકે છે. અંતે તો, દરેક async બ્લોક કંઈપણ પરત કરતું નથી, તેથી તે બધા `Future<Output = ()>` ઉત્પન્ન કરે છે. યાદ રાખો કે `Future` એ trait છે, અને કમ્પાઇલર દરેક async બ્લોક માટે એક અનન્ય enum બનાવે છે, ભલે તેમની આઉટપુટ પ્રકારો સમાન હોય. જેમ તમે બે અલગ-અલગ handwritten structs ને `Vec` માં મૂકી શકતા નથી, તેમ તમે કમ્પાઇલર દ્વારા જનરેટ કરેલા enums ને પણ મિક્સ કરી શકતા નથી.

પછી આપણે ભવિષ્યનો સમૂહ `trpl::join_all` વિધેયને આપીએ છીએ અને પરિણામની રાહ જોઈએ છીએ. જો કે, આ કમ્પાઇલ થતું નથી; અહીં ભૂલ સંદેશાઓનો સંબંધિત ભાગ છે.

<!-- manual-regeneration
cd listings/ch17-async-await/listing-17-23
cargo build
copy *only* the final `error` block from the errors
-->
```text
```text
error[E0277]: `dyn Future<Output = ()>` cannot be unpinned
  --> src/main.rs:48:33
   |
48 |         trpl::join_all(futures).await;
   |                                 ^^^^^ the trait `Unpin` is not implemented for `dyn Future<Output = ()>`
   |
   = note: consider using the `pin!` macro
           consider using `Box::pin` if you need to access the pinned value outside of the current scope
   = note: required for `Box<dyn Future<Output = ()>>` to implement `Future`
note: required by a bound in `futures_util::future::join_all::JoinAll`
  --> file:///home/.cargo/registry/src/index.crates.io-1949cf8c6b5b557f/futures-util-0.3.30/src/future/join_all.rs:29:8
   |
27 | pub struct JoinAll<F>
   |            ------- required by a bound in this struct
28 | where
29 |     F: Future,
   |        ^^^^^^ required by this bound in `JoinAll`
```
```
આ ભૂલ સંદેશમાં આપેલ નોંધ જણાવે છે કે આપણે `pin!` મેક્રોનો ઉપયોગ કરીને મૂલ્યોને પિન કરવા જોઈએ, જેનો અર્થ થાય છે તેમને `Pin` પ્રકારની અંદર મૂકવા, જે ખાતરી આપે છે કે મૂલ્યો સ્મૃતિમાં ખસેડવામાં આવશે નહીં. ભૂલ સંદેશ જણાવે છે કે પિનિંગ જરૂરી છે કારણ કે `dyn Future<Output = ()>` ને `Unpin` લક્ષણ લાગુ કરવાની જરૂર છે અને હાલમાં તે નથી.

`trpl::join_all` વિધેય એક struct પરત કરે છે જેને `JoinAll` કહેવાય છે. તે struct પ્રકાર `F` પર સામાન્ય છે, જે `Future` લક્ષણને અમલમાં મૂકવા માટે મર્યાદિત છે. `await` સાથે સીધું ભવિષ્યની રાહ જોવાવાથી તે આપમેળે પિન થાય છે. તેથી જ આપણે દરેક જગ્યાએ જ્યાં ભવિષ્યની રાહ જોવાની હોય ત્યાં `pin!` નો ઉપયોગ કરવાની જરૂર નથી.

જો કે, અહીં અમે સીધા ભવિષ્યની રાહ જોઈ રહ્યા નથી. તેના બદલે, અમે `join_all` વિધેયને ભવિષ્યના સંગ્રહ પસાર કરીને એક નવું ભવિષ્ય, JoinAll, બનાવીએ છીએ. `join_all` માટે હસ્તાક્ષર આવશ્યક કરે છે કે સંગ્રહમાં રહેલાં ઘટકોના પ્રકારો બધા `Future` લક્ષણનો અમલ કરે, અને `Box<T>` માત્ર ત્યારે જ `Future` નો અમલ કરે જો તે `T` જે રૅપ કરે છે તે `Unpin` લક્ષણનો અમલ કરતું ભવિષ્ય હોય.

ઘણું સમજવું પડશે! ખરેખર સમજવા માટે, ચાલો થોડું ઊંડાણપૂર્વક જોઈએ કે `Future` લક્ષણ ખરેખર કેવી રીતે કાર્ય કરે છે, વિશેષ કરીને પિનિંગની આસપાસ. ફરીથી `Future` લક્ષણની વ્યાખ્યા જુઓ:

```rust
```rust
use std::pin::Pin;
use std::task::{Context, Poll};

pub trait Future {
    type Output;

    // Required method
    fn poll(self: Pin<&mut Self>, cx: &mut Context<'_>) -> Poll<Self::Output>;
}
```
```
`cx` પરિમાણ અને તેનું `Context` પ્રકાર એ ચાવીરૂપ છે કે કેવી રીતે રનટાઇમ જાણે છે ક્યારે કોઈ ચોક્કસ ભવિષ્ય તપાસવું, તેમ છતાં તે આળસુ રહે છે. ફરીથી, તે કેવી રીતે કાર્ય કરે છે તેની વિગતો આ પ્રકરણના અવકાશની બહાર છે, અને તમારે સામાન્ય રીતે માત્ર ત્યારે જ આ વિશે વિચારવાની જરૂર છે જ્યારે તમે કસ્ટમ `Future` અમલીકરણ લખી રહ્યા હોવ. આપણે તેના બદલે `self` માટેના પ્રકાર પર ધ્યાન કેન્દ્રિત કરીશું, કારણ કે આ પ્રથમ વખત છે જ્યારે આપણે એક એવી પદ્ધતિ જોઈ રહ્યા છીએ જ્યાં `self` પાસે પ્રકારની નોંધણી છે. `self` માટેની પ્રકારની નોંધણી અન્ય ફંક્શન પરિમાણો માટેની પ્રકારની નોંધણીઓ જેવી જ કાર્ય કરે છે પરંતુ બે મુખ્ય તફાવતો સાથે:

તે Rust ને જણાવે છે કે પદ્ધતિને બોલાવવા માટે `self` કયા પ્રકારનું હોવું

જોઈએ. તે કોઈપણ પ્રકારનું ન હોઈ શકે. તે અમલમાં મૂકાયેલ પ્રકાર, તે પ્રકારનો સંદર્ભ અથવા સ્માર્ટ પોઇન્ટર, અથવા `Pin` જે તે પ્રકારના સંદર્ભને આવરી લે છે તેના સુધી મર્યાદિત છે.

અમે આ સિન્ટેક્સ વિશે પ્રકરણ ૧૮ માં વધુ જોઈશું. હાલ માટે, એ જાણવું પૂરતું છે કે જો આપણે ચકાસવા માટે ફ્યુચરને પોલ કરવા માંગતા હોઈએ કે તે `Pending` છે કે `Ready(Output)` , તો આપણને `Pin`-રેપ કરેલા મ્યુટેબલ રેફરન્સની જરૂર પડશે જે પ્રકારનું હોય.

`Pin` એ પોઇન્ટર-જેવા પ્રકારો માટેનું આવરણ છે, જેમ કે `&`, `&mut`, `Box`, અને `Rc`. (તકનીકી રીતે, `Pin` એવા પ્રકારો સાથે કામ કરે છે જે `Deref` અથવા `DerefMut` ટ્રેઇટ્સનો અમલ કરે છે, પરંતુ આ માત્ર રેફરન્સ અને સ્માર્ટ પોઇન્ટર્સ સાથે કામ કરવા સમાન છે.) `Pin` પોતે કોઈ પોઇન્ટર નથી અને તેમાં કોઈ વર્તન નથી જેવું `Rc` અને `Arc` રેફરન્સ ગણતરી સાથે કરે છે; તે સંપૂર્ણપણે એક સાધન છે જેનો કમ્પાઇલર પોઇન્ટર વપરાશ પર નિયંત્રણો લાદવા માટે ઉપયોગ કરી શકે છે.

યાદ રાખો કે `await` ને `poll` કૉલ્સના સંદર્ભમાં અમલમાં મૂકવામાં આવે છે, તે અગાઉ આપણે જોયેલ ભૂલ સંદેશ સમજાવવાનું શરૂ કરે છે, પરંતુ તે `Unpin` ના સંદર્ભમાં હતું, `Pin` નો નહીં. તો `Pin` અને `Unpin` વચ્ચેનો સંબંધ શું છે, અને શા

માટે `Future` ને `poll` કૉલ કરવા માટે `self` ને `Pin` પ્રકારમાં હોવું જરૂરી છે? યાદ રાખો કે આ પ્રકરણમાં અગાઉ, ભવિષ્યના અવેઇટ પોઈન્ટ્સની શ્રેણીને સ્ટેટ મશીનમાં કમ્પાઇલ કરવામાં આવે છે, અને કમ્પાઈલર ખાતરી કરે છે કે તે સ્ટેટ મશીન Rust ના સામાન્ય સલામતી નિયમોનું પાલન કરે છે, જેમાં બોરોઇંગ અને ઓવ્નરશિપનો સમાવેશ થાય છે. આ કાર્ય કરવા માટે, Rust એક અવેઇટ પોઈન્ટથી બીજા અવેઇટ પોઈન્ટ અથવા એસિંક બ્લોકના અંત સુધી જરૂરી ડેટા શું છે તે જુએ છે. પછી તે કમ્પાઈલ કરેલા સ્ટેટ મશીનમાં અનુરૂપ વેરિઅન્ટ બનાવે છે. દરેક વેરિઅન્ટને સ્રોત કોડના તે વિભાગમાં વપરાયેલા ડેટાની ઍક્સેસ મળે છે, કાં તો તે ડેટાનું ઓવ્નરશિપ લઈને અથવા તેને મ્યુટેબલ અથવા ઇમ્યુટેબલ રેફરન્સ મેળવીને.

આપણે ત્યાં સુધી બધું સારું છે: જો આપણે કોઈ પણ `ownership` અથવા `reference` વિશે ભૂલ કરીએ છીએ, તો `borrow checker` આપણને જણાવશે. જ્યારે આપણે તે બ્લોકને અનુરૂપ ભવિષ્યને ખસેડવા માંગીએ છીએ—જેમ કે તેને

`Vec` માં ખસેડીને `join_all` ને પસાર કરવા—તો બાબતો વધુ જટિલ બની જાય છે. જ્યારે આપણે કોઈ ભવિષ્યને ખસેડીએ છીએ—ભલે તે ડેટા સ્ટ્રક્ચરમાં ધકેલીને `join_all` સાથે ઇટરેટર તરીકે ઉપયોગ કરવા માટે હોય અથવા ફંક્શનમાંથી તેને પરત કરીને—તો તેનો અર્થ એ થાય છે કે આપણે `Rust` આપણી માટે બનાવેલ સ્ટેટ મશીનને ખસેડીએ છીએ. અને `Rust` માં મોટાભાગના અન્ય પ્રકારોથી વિપરીત, `async` બ્લોક્સ માટે `Rust` બનાવેલા ભવિષ્યમાં કોઈપણ આપેલ વિવિધતાના ક્ષેત્રોમાં પોતાની જાતનાં સંદર્ભો હોઈ શકે છે, જે આકૃતિ 17-4 માં દર્શાવેલ સરળ ચિત્રમાં બતાવ્યા પ્રમાણે છે.

<figure>
<img alt="A single-column, three-row table representing a future, fut1, which has data values 0 and 1 in the first two rows and an arrow pointing from the third row back to the second row, representing an internal reference within the future." src="img/trpl17-04.svg" class="center" />
<figcaption>Figure 17-4: A self-referential data type</figcaption>
</figure>
સામાન્ય રીતે, જો કે, પોતાની જાતને નિર્દેશ કરતા કોઈપણ વસ્તુને ખસેડવી અસુરક્ષિત છે, કારણ કે સંદર્ભ હંમેશાં જેની તરફ તે નિર્દેશ કરે છે તે સ્મૃતિ સરનામા (memory address) પર નિર્દેશ કરે છે (આકૃતિ ૧૭-૫ જુઓ). જો તમે ડેટા સ્ટ્રક્ચરને ખસેડો છો, તો તે આંતરિક સંદર્ભો જૂના સ્થાન તરફ નિર્દેશ કરતા રહેશે. જો કે, તે સ્મૃતિ સ્થાન હવે અમાન્ય છે. એક વાત એ છે કે, જ્યારે તમે ડેટા સ્ટ્રક્ચરમાં ફેરફાર કરો છો, ત્યારે તેની કિંમત અપડેટ થશે નહીં. બીજી—વધુ મહત્વની—વાત એ છે કે, કમ્પ્યુટર હવે તે સ્મૃતિને અન્ય હેતુઓ માટે વાપરવા માટે મુક્ત છે! તમે પાછળથી સંપૂર્ણપણે અસંબંધિત ડેટા વાંચી શકો છો.

<figure>
<img alt="Two tables, depicting two futures, fut1 and fut2, each of which has one column and three rows, representing the result of having moved a future out of fut1 into fut2. The first, fut1, is grayed out, with a question mark in each index, representing unknown memory. The second, fut2, has 0 and 1 in the first and second rows and an arrow pointing from its third row back to the second row of fut1, representing a pointer that is referencing the old location in memory of the future before it was moved." src="img/trpl17-05.svg" class="center" />
<figcaption>Figure 17-5: The unsafe result of moving a self-referential data type</figcaption>
</figure>
સૈદ્ધાંતિક રીતે, Rust compiler દરેક સંદર્ભને કોઈ વસ્તુ તરફ ખસેડતી વખતે અપડેટ કરવાનો પ્રયત્ન કરી શકે છે, પરંતુ તેનાથી ઘણું કામગીરી ભાર વધી શકે છે, વિશેષ કરીને જો સંદર્ભોનું જાળું અપડેટ કરવાની જરૂર હોય તો. જો આપણે ખાતરી કરી શકીએ કે પ્રશ્નમાં રહેલી માહિતી રચના સ્થાનાંતરિત થતી નથી, તો આપણે કોઈ પણ સંદર્ભને અપડેટ કરવાની જરૂર રહેશે નહીં. આ જ Rust ના borrow checker નું કાર્ય છે: સુરક્ષિત કોડમાં, તે તમને કોઈપણ વસ્તુને ખસેડતા અટકાવે છે જેના માટે સક્રિય સંદર્ભ છે.

`Pin` તે પર આધારિત ચોક્કસ ખાતરી આપે છે જેની આપણને જરૂર છે. જ્યારે આપણે કોઈ મૂલ્યને `Pin` માં pointer લપેટીને pin કરીએ છીએ, ત્યારે તે ખસેડી શકાતું નથી. આમ, જો તમારી પાસે `Pin<Box<SomeType>>` હોય, તો તમે `SomeType` મૂલ્યને pin કરો છો, `Box` pointer ને નહીં. આ પ્રક્રિયા આકૃતિ 17-6 માં દર્શાવવામાં આવી છે.

<figure>
<img alt="Three boxes laid out side by side. The first is labeled “Pin”, the second “b1”, and the third “pinned”. Within “pinned” is a table labeled “fut”, with a single column; it represents a future with cells for each part of the data structure. Its first cell has the value “0”, its second cell has an arrow coming out of it and pointing to the fourth and final cell, which has the value “1” in it, and the third cell has dashed lines and an ellipsis to indicate there may be other parts to the data structure. All together, the “fut” table represents a future which is self-referential. An arrow leaves the box labeled “Pin”, goes through the box labeled “b1” and terminates inside the “pinned” box at the “fut” table." src="img/trpl17-06.svg" class="center" />
<figcaption>Figure 17-6: Pinning a `Box` that points to a self-referential future type</figcaption>
</figure>
અસલમાં, `Box` પોઇન્ટર હજી પણ સ્વતંત્ર રીતે ખસી શકે છે. યાદ રાખો: આપણે એ સુનિશ્ચિત કરવા પર ધ્યાન કેન્દ્રિત કરીએ છીએ કે અંતિમ રીતે જે ડેટાનો સંદર્ભ લેવામાં આવે છે તે તેની જગ્યાએ રહે. જો કોઈ પોઇન્ટર ખસે છે, પરંતુ તે જે ડેટા તરફ નિર્દેશ કરે છે તે સમાન જગ્યાએ હોય, જેમ કે આકૃતિ 17-7 માં દર્શાવેલ છે, તો કોઈ સંભવિત સમસ્યા નથી. (સ્વતંત્ર કવાયતના ભાગ રૂપે, પ્રકારો માટેના દસ્તાવેજો તેમજ `std::pin` મોડ્યુલ જુઓ અને પ્રયત્ન કરો કે તમે `Pin` વડે `Box` ને લપેટીને આ કેવી રીતે કરી શકો.) મહત્વની વાત એ છે કે સ્વ-સંદર્ભિત પ્રકાર પોતે જ ખસી શકતો નથી, કારણ કે તે હજી પણ પિન કરેલો છે.

<figure>
<img alt="Four boxes laid out in three rough columns, identical to the previous diagram with a change to the second column. Now there are two boxes in the second column, labeled “b1” and “b2”, “b1” is grayed out, and the arrow from “Pin” goes through “b2” instead of “b1”, indicating that the pointer has moved from “b1” to “b2”, but the data in “pinned” has not moved." src="img/trpl17-07.svg" class="center" />
<figcaption>Figure 17-7: Moving a `Box` which points to a self-referential future type</figcaption>
</figure>
જો કે, મોટાભાગના પ્રકારોને ખસેડવા માટે સંપૂર્ણપણે સુરક્ષિત છે, ભલે તે `Pin` પોઇન્ટર પાછળ હોય. આપણે માત્ર પિનિંગ વિશે વિચારવાની જરૂર છે જ્યારે આઇટમ્સમાં આંતરિક સંદર્ભો હોય. સંખ્યાઓ અને બુલિયન જેવી પ્રાથમિક કિંમતો સુરક્ષિત છે કારણ કે તેમાં કોઈ આંતરિક સંદર્ભો નથી. મોટાભાગના પ્રકારો જેની સાથે તમે સામાન્ય રીતે Rust માં કામ કરો છો તે પણ સુરક્ષિત છે. ઉદાહરણ તરીકે, તમે `Vec` ને ખસેડી શકો છો, ચિંતા કર્યા વિના. અત્યાર સુધી આપણે જે જોયું છે, જો તમારી પાસે `Pin<Vec<String>>` હોય, તો તમારે `Pin` દ્વારા પૂરા પાડવામાં આવેલા સુરક્ષિત પરંતુ પ્રતિબંધક API નો ઉપયોગ કરવો પડશે, ભલે `Vec<String>` હંમેશાં સુરક્ષિત હોય જો તેના પર અન્ય કોઈ સંદર્ભો ન હોય. આપણે કમ્પાઇલરને જણાવવાની એક રીત જોઈએ કે આ પ્રકારના કિસ્સાઓમાં આઇટમ્સને ખસેડવું ઠીક છે—અને તે જ જગ્યાએ `Unpin` આવે છે.

`Unpin` એ એક નિશાની ટ્રેઇટ છે, જે `Send` અને `Sync` ટ્રેઇટ્સ જેવો જ છે જેને આપણે પ્રકરણ ૧૬ માં જોયો હતો, અને તેથી તેની પોતાની કોઈ કાર્યક્ષમતા નથી. નિશાની ટ્રેઇટ્સ માત્ર કમ્પાઇલરને જણાવવા માટે અસ્તિત્વ ધરાવે છે કે આપેલ ટ્રેઇટનો અમલ કરતી પ્રકારને ચોક્કસ સંદર્ભમાં સુરક્ષિત રીતે વાપરી શકાય છે. `Unpin` કમ્પાઇલરને માહિતગાર કરે છે કે આપેલ પ્રકારને કોઈ ખાતરી રાખવાની જરૂર નથી કે પ્રશ્નમાં રહેલા મૂલ્યને સુરક્ષિત રીતે ખસેડી શકાય છે.

<!--
  The inline `<code>` in the next block is to allow the inline `<em>` inside it,
  matching what NoStarch does style-wise, and emphasizing within the text here
  that it is something distinct from a normal type.
-->
જેમ કે `Send` અને `Sync` સાથે, કમ્પાઇલર આપોઆપ જ `Unpin` ને તમામ પ્રકારો માટે અમલમાં મૂકે છે જ્યાં તે સાબિત કરી શકે છે કે તે સુરક્ષિત છે. એક વિશેષ સ્થિતિ, ફરીથી `Send` અને `Sync` જેવી જ, એ છે કે જ્યાં `Unpin` કોઈ પ્રકાર માટે અમલમાં નથી. આ માટેની નોંધણી આ પ્રમાણે છે: `impl !Unpin for SomeType`, જ્યાં `SomeType` એ પ્રકારનું નામ છે જેને તે સુરક્ષાની ખાતરીઓ જાળવવાની જરૂર છે જ્યારે તે પ્રકારના પોઇન્ટરનો ઉપયોગ `Pin` માં થાય છે.

અર્થાત, `Pin` અને `Unpin` વચ્ચેના સંબંધને ધ્યાનમાં રાખવા માટે બે બાબતો છે. પ્રથમ, `Unpin` એ "સામાન્ય" સ્થિતિ છે, અને `!Unpin` એ વિશેષ સ્થિતિ છે. બીજું, કોઈ પ્રકાર `Unpin` અથવા `!Unpin` અમલમાં મૂકે છે કે નહીં તે માત્ર ત્યારે જ મહત્વ ધરાવે છે જ્યારે તમે તે પ્રકારના પિન કરેલા પોઇન્ટરનો ઉપયોગ કરી રહ્યા હોવ, જેમ કે `Pin < &mut SomeType >`.

તેને નક્કર બનાવવા માટે,  `String` વિશે વિચારો: તેની લંબાઈ અને યુનિકોડ અક્ષરો હોય છે જે તેને બનાવે છે. આપણે Figure 17-8 માં જોયા પ્રમાણે `String` ને `Pin` માં લપેટી શકીએ છીએ. જો કે, `String` આપમેળે `Unpin` અમલમાં મૂકે છે, મોટાભાગના અન્ય પ્રકારો પણ Rust માં આ જ કરે છે.

<figure>
<img alt="A box labeled “Pin” on the left with an arrow going from it to a box labeled “String” on the right. The “String” box contains the data 5usize, representing the length of the string, and the letters “h”, “e”, “l”, “l”, and “o” representing the characters of the string “hello” stored in this String instance. A dotted rectangle surrounds the “String” box and its label, but not the “Pin” box." src="img/trpl17-08.svg" class="center" />
<figcaption>Figure 17-8: Pinning a `String`; the dotted line indicates that the `String` implements the `Unpin` trait and thus is not pinned</figcaption>
</figure>
પરિણામ સ્વરૂપે, આપણે એવી ક્રિયાઓ કરી શકીએ છીએ જે `String` દ્વારા `!Unpin` અમલમાં મૂકવામાં આવે તો ગેરકાયદેસર ગણાત. જેમ કે આકૃતિ ૧૭-૯ માં દર્શાવ્યા પ્રમાણે, એક જ સ્થાને મેમરીમાં સ્ટ્રિંગને બદલવી. આ `Pin` સંધિનું ઉલ્લંઘન કરતું નથી, કારણ કે `String` પાસે કોઈ આંતરિક સંદર્ભો નથી જે તેને ખસેડવામાં અસુરક્ષિત બનાવે છે. એ જ કારણે તે `Unpin` અમલમાં મૂકે છે, `!Unpin` નહીં.

<figure>
<img alt="The same “hello” string data from the previous example, now labeled “s1” and grayed out. The “Pin” box from the previous example now points to a different String instance, one that is labeled “s2”, is valid, has a length of 7usize, and contains the characters of the string “goodbye”. s2 is surrounded by a dotted rectangle because it, too, implements the Unpin trait." src="img/trpl17-09.svg" class="center" />
<figcaption>Figure 17-9: Replacing the `String` with an entirely different `String` in memory</figcaption>
</figure>
હવે આપણને પૂરતું જ્ઞાન છે કે Listing 17-23 માં પાછળના `join_all` કૉલ માટે રિપોર્ટ થયેલી ભૂલોને સમજવા માટે. આપણે મૂળરૂપે async બ્લોક્સ દ્વારા ઉત્પાદિત ભવિષ્યને `Vec<Box<dyn Future<Output = ()>>>` માં ખસેડવાનો પ્રયત્ન કર્યો હતો, પરંતુ આપણે જોયું છે તેમ, તે ભવિષ્યમાં આંતરિક સંદર્ભો હોઈ શકે છે, તેથી તેઓ આપમેળે `Unpin` લાગુ કરતા નથી. એકવાર આપણે તેમને પિન કરીએ, પછી આપણે પરિણામી `Pin` પ્રકારને `Vec` માં આપી શકીએ છીએ, એ વાતનો વિશ્વાસ રાખીને કે ભવિષ્યમાં રહેલાં અંતર્ગત ડેટા ખસેડવામાં આવશે નહીં. Listing 17-24 બતાવે છે કે દરેક ત્રણ ભવિષ્ય વ્યાખ્યાયિત કરવામાં આવે ત્યારે `pin!` મેક્રો કૉલ કરીને અને ટ્રેઇટ ઓબ્જેક્ટ પ્રકારને સમાયોજિત કરીને કોડને કેવી રીતે સુધારવો.

<Listing number="17-24" caption="Pinning the futures to enable moving them into the vector">
```rust
```rust
{{#rustdoc_include ../listings/ch17-async-await/listing-17-24/src/main.rs:here}}
```
```
</Listing>
આ ઉદાહરણ હવે સંપાઈ જાય છે અને ચાલે છે, અને અમે ચલિતકાળમાં વેક્ટર માંથી ભવિષ્ય ઉમેરી અથવા દૂર કરી શકીએ છીએ અને બધાને જોડી શકીએ છીએ.

`Pin` અને `Unpin` મોટા ભાગે નીચલા સ્તરના લાયબ્રેરીઓ બનાવવા માટે મહત્વપૂર્ણ છે, અથવા જ્યારે તમે ચલિતકાળ જાતે બનાવી રહ્યા હોવ, દૈનિક Rust કોડ માટે નહીં. પરંતુ, જ્યારે તમને ભૂલ સંદેશાઓમાં આ traits દેખાય છે, તો હવે તમને તમારા કોડને સુધારવાનો વધુ સારો ખ્યાલ આવશે!

નોંધ: `Pin` અને `Unpin` નું આ સંયોજન એ શક્ય બનાવે છે કે Rust માં જટિલ પ્રકારોની એક સંપૂર્ણ શ્રેણી સુરક્ષિત રીતે અમલમાં મૂકી શકાય છે જે અન્યથા મુશ્કેલ સાબિત થશે કારણ કે તે સ્વ-સંદર્ભિત છે. `Pin` જરૂરી હોય તેવા પ્રકારો આજે async Rust માં સૌથી સામાન્ય રીતે દેખાય છે, પરંતુ ક્યારેક-ક્યારેક તમે તેને અન્ય સંદર્ભોમાં પણ જોઈ શકો છો.

`Pin` અને `Unpin` કેવી રીતે કાર્ય કરે છે તેની વિગતો, અને તેઓ જે નિયમોનું પાલન કરવા માટે બંધાયેલા છે તે વિશેની માહિતી, `std::pin` ના API દસ્તાવેજોમાં વિસ્તૃતપણે વર્ણવવામાં આવી છે, તેથી જો તમને વધુ જાણવામાં રસ હોય, તો તે શરૂ કરવા માટે

એક ઉત્તમ સ્થળ છે. If you want to understand how things work under the hood in even more detail, see Chapters 2 and 4 of Asynchronous Programming in Rust . જો તમે વધુ વિગતવાર જાણવા માંગતા હોવ કે વસ્તુઓ કેવી રીતે કાર્ય કરે છે, તો Rust માં અસિંક્રોનસ પ્રોગ્રામિંગના પ્રકરણો ૨ અને ૪ જુઓ.

### The `Stream` Trait

હવે જ્યારે તમને `Future`, `Pin`, અને `Unpin` લક્ષણો વિશે ઊંડી સમજણ આવી ગઈ છે, ત્યારે આપણે `Stream` લક્ષણ તરફ ધ્યાન આપી શકીએ છીએ. તમે અગાઉ આ પ્રકરણમાં શીખ્યા મુજબ, સ્ટ્રીમ્સ એસમિંક્રોનસ ઇટરેટર્સ જેવા જ હોય છે. જો કે, `Iterator` અને `Future` ની જેમ, `Stream` નું સ્ટાન્ડર્ડ લાઈબ્રેરીમાં કોઈ વ્યાખ્યા નથી, પરંતુ `futures` ક્રેઇટમાંથી એક સામાન્ય વ્યાખ્યા છે જે સમગ્ર ઇકોસિસ્ટમમાં વપરાય છે.

ચાલો આપણે `Iterator` અને `Future` લક્ષણોની વ્યાખ્યાઓ પર નજર કરીએ, તે પહેલાં જોઈએ કે `Stream` લક્ષણ કેવી રીતે તેમને જોડી શકે છે. `Iterator` માંથી, આપણને ક્રમનો ખ્યાલ મળે છે: તેની `next` પદ્ધતિ `Option<Self::Item>` પ્રદાન કરે છે. `Future` માંથી, આપણને સમય જતાં તૈયારીનો ખ્યાલ મળે છે: તેની `poll` પદ્ધતિ `Poll<Self::Output>` પ્રદાન કરે છે. સમય જતાં તૈયાર થતી વસ્તુઓની શ્રેણીનું પ્રતિનિધિત્વ કરવા માટે, અમે એક `Stream` લક્ષણ વ્યાખ્યાયિત કરીએ છીએ જે આ બંને લક્ષણોને જોડે છે:

```rust
```rust
use std::pin::Pin;
use std::task::{Context, Poll};

trait Stream {
    type Item;

    fn poll_next(
        self: Pin<&mut Self>,
        cx: &mut Context<'_>
    ) -> Poll<Option<Self::Item>>;
}
```
```
Stream લક્ષણ વ્યાખ્યાયિત કરે છે એક સંકળાયેલ પ્રકાર જેવું કે `Item`, જે પ્રવાહ દ્વારા ઉત્પન્ન થતા ઘટકોનો પ્રકાર દર્શાવે છે. આ `Iterator` જેવું જ છે, જેમાં શૂન્યથી ઘણાં ઘટકો હોઈ શકે છે, અને `Future` થી અલગ છે, જ્યાં હંમેશા એક જ `Output` હોય છે, ભલે તે એકમ પ્રકાર `()` હોય.

`Stream` એ પણ એક પદ્ધતિ વ્યાખ્યાયિત કરે છે જે તે ઘટકો મેળવે છે. અમે તેને `poll_next` કહીએ છીએ, જેથી સ્પષ્ટ થાય કે તે `Future::poll` ની જેમ જ પોલ કરે છે અને `Iterator::next` ની જેમ જ ઘટકોની શ્રેણી ઉત્પન્ન કરે છે. તેનું વળતર પ્રકાર `Poll` સાથે `Option` નું મિશ્રણ છે. બાહ્ય પ્રકાર `Poll` છે, કારણ કે તેની તૈયારી તપાસવી જરૂરી છે, જેવું કે ભવિષ્યમાં હોય છે. આંતરિક પ્રકાર `Option` છે, કારણ કે તેને વધુ સંદેશાઓ છે કે નહીં તે દર્શાવવાની જરૂર છે, જેવું કે ઇટરેટર કરે છે.

કોઈ વસ્તુ આ વ્યાખ્યા સાથે ઘણું મળતું આવે તેવી શક્યતા છે કે તે Rust ના પ્રમાણિત પુસ્તકાલયનો ભાગ બની જશે. ત્યાં સુધી, તે મોટાભાગના રનટાઇમ ટૂલકીટનો ભાગ છે, તેથી તમે તેના પર આધાર રાખી શકો છો, અને આવનાર દરેક બાબત સામાન્ય રીતે લાગુ થશે!

જો કે, આપણે “સ્ટ્રીમ્સ: ફ્યુચર્સ ઇન સિક્વન્સ” વિભાગમાં જોયેલી ઉદાહરણોમાં, આપણે `poll_next` અથવા `Stream` નો ઉપયોગ કર્યો ન હતો, પરંતુ તેના બદલે `next` અને `StreamExt` નો ઉપયોગ કર્યો હતો. અલબત્ત, આપણે જાતે `Stream` સ્ટેટ મશીનો લખીને `poll_next` API સાથે સીધા જ કામ કરી શકીએ છીએ, જેમ કે આપણે તેમના `poll` પદ્ધતિ દ્વારા ફ્યુચર્સ સાથે સીધા જ કામ કરી શકીએ છીએ. જો કે, `await` નો ઉપયોગ કરવો ઘણો સારો છે, અને `StreamExt` ટ્રેઇટ `next` પદ્ધતિ પૂરી પાડે છે જેથી આપણે તેવું કરી શકીએ:

```rust
```rust
{{#rustdoc_include ../listings/ch17-async-await/no-listing-stream-ext/src/lib.rs:here}}
```
```
<!--
TODO: update this if/when tokio/etc. update their MSRV and switch to using async functions
in traits, since the lack thereof is the reason they do not yet have this.
-->
નોંધ: અગાઉના પ્રકરણમાં આપેલ વ્યાખ્યા આથી થોડી અલગ દેખાય છે, કારણ કે તે Rust ના એવા વર્ઝન માટે સપોર્ટ કરે છે જેણે હજી સુધી ટ્રેઇટમાં async ફંક્શન વાપરવાનું સપોર્ટ નહોતું કર્યું. તેથી, તે આ પ્રમાણે દેખાય છે:

fn next(&mut self) -> Next<'_, Self> where Self: Unpin;
તે `Next` પ્રકાર એક `struct` છે જે `Future` અમલમાં મૂકે છે અને આપણને `self` ના સંદર્ભના આયુષ્યને `Next<'_, Self>` સાથે નામ આપવા દે છે, જેથી `await` આ પદ્ધતિ સાથે કાર્ય કરી શકે. The

લક્ષણ તમામ રસપ્રદ પદ્ધતિઓનું ઘર પણ છે જે પ્રવાહો સાથે ઉપયોગ માટે ઉપલબ્ધ છે. `StreamExt` આપોઆપ દરેક પ્રકાર માટે અમલમાં મૂકાય છે જે `Stream` અમલમાં મૂકે છે, પરંતુ આ લક્ષણો અલગથી વ્યાખ્યાયિત કરવામાં આવે છે જેથી સમુદાય મૂળભૂત લક્ષણ પર અસર કર્યા વિના સુવિધા API પર પુનરાવર્તન કરી શકે.

`trpl` ક્રેટમાં વપરાયેલ `StreamExt` ના સંસ્કરણમાં, આ ટ્રેઇટ માત્ર `next` પદ્ધતિને વ્યાખ્યાયિત જ નથી કરતું, પરંતુ `Stream::poll_next` બોલાવવાની વિગતોને યોગ્ય રીતે નિયંત્રિત કરતા `next` ના ડિફોલ્ટ અમલીકરણ (implementation) પણ પૂરા પાડે છે. આનો અર્થ એ થાય છે કે જ્યારે તમારે તમારી પોતાની સ્ટ્રીમિંગ ડેટા પ્રકાર લખવાની જરૂર હોય, ત્યારે તમારે માત્ર `Stream` નો અમલ કરવો પડે છે, અને પછી કોઈપણ વ્યક્તિ જે તમારા ડેટા પ્રકારનો ઉપયોગ કરે છે તે આપોઆપ `StreamExt` અને તેની પદ્ધતિઓનો ઉપયોગ કરી શકે છે. That’s all we’re going to cover for the

આ ટ્રેઇટ્સની નીચલા સ્તરની વિગતો માટે આટલું જ પૂરતું છે. સમાપક તરીકે, ચાલો જોઈએ કે ફ્યુચર્સ (સ્ટ્રીમ્સ સહિત), કાર્યો અને થ્રેડ્સ કેવી રીતે એકસાથે બંધાયેલા છે!

