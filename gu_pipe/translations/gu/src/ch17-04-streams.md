<!-- Old headings. Do not remove or links may break. -->
## Streams: Futures in Sequence

યાદ કરો કે આપણે અગાઉ આ પ્રકરણના “સંદેશાવ્યવહાર” વિભાગમાં આપણી async ચેનલ માટે રીસીવરનો ઉપયોગ કેવી રીતે કર્યો હતો. Async `recv` પદ્ધતિ સમય જતાં વસ્તુઓની શ્રેણી ઉત્પન્ન કરે છે. આ એક વધુ સામાન્ય પેટર્નનું ઉદાહરણ છે જેને પ્રવાહ કહેવામાં આવે છે. ઘણી વિભાવનાઓને સ્વાભાવિક રીતે પ્રવાહો તરીકે રજૂ કરી શકાય છે: કતારમાં ઉપલબ્ધ થતી વસ્તુઓ, ફાઇલસિસ્ટમમાંથી ક્રમશઃ ડેટાના ટુકડા ખેંચીને લાવવામાં આવે છે જ્યારે સંપૂર્ણ ડેટાસેટ કમ્પ્યુટરની મેમરી માટે ખૂબ મોટો હોય, અથવા નેટવર્ક પર સમય જતાં આવતો ડેટા. કારણ કે પ્રવાહો futures છે, અમે તેનો ઉપયોગ અન્ય કોઈપણ પ્રકારના future સાથે કરી શકીએ છીએ અને તેને રસપ્રદ રીતે જોડી શકીએ છીએ. ઉદાહરણ તરીકે, આપણે ઘણા બધા નેટવર્ક કૉલ્સને ટાળવા માટે ઘટનાઓને જૂથબદ્ધ કરી શકીએ છીએ, લાંબા સમય સુધી ચાલતા કામગીરીની શ્રેણીઓ પર સમયમર્યાદા સેટ કરી શકીએ છીએ અથવા બિનજરૂરી કાર્ય કરવાનું ટાળવા માટે user ઇન્ટરફેસની ઘટનાઓને નિયંત્રિત કરી શકીએ છીએ.

અમે પ્રકરણ ૧૩ માં એક વસ્તુઓની શ્રેણી જોઈ હતી, જ્યારે અમે [“The Iterator Trait and the `next` Method”][iterator-trait] વિભાગમાં Iterator trait ને તપાસ્યું હતું, પરંતુ iterator અને async channel receiver વચ્ચે બે તફાવત છે. પ્રથમ તફાવત સમયનો છે: iterators synchronous હોય છે, જ્યારે channel receiver asynchronous હોય છે. બીજો તફાવત API નો છે. `Iterator` સાથે સીધું કાર્ય કરતી વખતે, અમે તેનું synchronous `next` પદ્ધતિને બોલાવીએ છીએ. `trpl::Receiver` સ્ટ્રીમ સાથે વિશેષ કરીને, અમે એક asynchronous `recv` પદ્ધતિને બદલે બોલાવી હતી. અન્યથા, આ APIs ખૂબ સમાન લાગે છે, અને તે સામ્યતા કોઈ સંયોગ નથી. સ્ટ્રીમ એ iteration નું asynchronous સ્વરૂપ જેવું છે. જો કે `trpl::Receiver` વિશેષ કરીને સંદેશો મેળવવા માટે રાહ જુએ છે, તો સામાન્ય હેતુની સ્ટ્રીમ API ઘણું વ્યાપક છે: તે `Iterator` ની જેમ જ આગલી વસ્તુ પ્રદાન કરે છે, પરંતુ asynchronously.

માં ઇટરેટર (iterator) અને સ્ટ્રીમ (stream) વચ્ચેની સમાનતાનો અર્થ એ થાય છે કે આપણે કોઈપણ ઇટરેટરથી સ્ટ્રીમ બનાવી શકીએ છીએ. એક ઇટરેટરની જેમ, આપણે તેની `next` પદ્ધતિને બોલાવીને અને પછી આઉટપુટની રાહ જોઈને સ્ટ્રીમ સાથે કાર્ય કરી શકીએ છીએ, જે યાદી 17-21માં દર્શાવેલ છે, જે હજી કમ્પાઇલ (compile) થશે નહીં.

<Listing number="17-21" caption="Creating a stream from an iterator and printing its values" file-name="src/main.rs">
```rust
{{#rustdoc_include ../listings/ch17-async-await/listing-17-21/src/main.rs:stream}}
```
</Listing>
અમે સંખ્યાઓની શ્રેણીથી આરંભ કરીએ છીએ, જેને આપણે પુનરાવર્તક (iterator) માં રૂપાંતરિત કરીએ છીએ અને પછી તમામ મૂલ્યોને બમણા કરવા માટે `map` ને બોલાવીએ છીએ. ત્યારબાદ અમે `trpl::stream_from_iter` વિધેયનો ઉપયોગ કરીને પુનરાવર્તકને પ્રવાહમાં ફેરવીએ છીએ. આગળ, આપણે `while let` લૂપ વડે આવતા આઇટમ્સ પર લૂપ કરીએ છીએ.

કમનસીબે, જ્યારે આપણે કોડ ચલાવવાનો પ્રયત્ન કરીએ છીએ, ત્યારે તે કમ્પાઇલ થતો નથી પરંતુ તેના બદલે જણાવે છે કે કોઈ `next` પદ્ધતિ ઉપલબ્ધ નથી:

<!-- manual-regeneration
cd listings/ch17-async-await/listing-17-21
cargo build
copy only the error output
-->
```text
```text
error[E0599]: no method named `next` found for struct `tokio_stream::iter::Iter` in the current scope
  --> src/main.rs:10:40
   |
10 |         while let Some(value) = stream.next().await {
   |                                        ^^^^
   |
   = help: items from traits can only be used if the trait is in scope
help: the following traits which provide `next` are implemented but not in scope; perhaps you want to import one of them
   |
1  + use crate::trpl::StreamExt;
   |
1  + use futures_util::stream::stream::StreamExt;
   |
1  + use std::iter::Iterator;
   |
1  + use std::str::pattern::Searcher;
   |
help: there is a method `try_next` with a similar name
   |
10 |         while let Some(value) = stream.try_next().await {
   |                                        ~~~~~~~~
```
```
આ આઉટપુટ સમજાવે છે તેમ, કમ્પાઇલરની ભૂલનું કારણ એ છે કે `next` પદ્ધતિનો ઉપયોગ કરવા માટે યોગ્ય ટ્રેઇટ કાર્યક્ષેત્રમાં હોવી જરૂરી છે. અત્યાર સુધીની આપણી ચર્ચાને ધ્યાનમાં રાખીને, તમે તે ટ્રેઇટ `Stream` હોવાની અપેક્ષા રાખી શકો છો, પરંતુ હકીકતમાં તે `StreamExt` છે. એક્સ્ટેંશન માટે ટૂંકું નામ, `Ext` એ Rust સમુદાયમાં એક સામાન્ય રીત છે જે અન્ય ટ્રેઇટ સાથે ટ્રેઇટને વિસ્તારવા માટે વપરાય છે.

ટ્રેઇટ એક નીચલા સ્તરનું ઇન્ટરફેસ વ્યાખ્યાયિત કરે છે જે અસરકારક રીતે `Iterator` અને `Future` ટ્રેઇટ્સને જોડે છે. `StreamExt` `Stream` ઉપર ઉચ્ચ-સ્તરના API નો સમૂહ પૂરો પાડે છે, જેમાં `next` પદ્ધતિ તેમજ `Iterator` ટ્રેઇટ દ્વારા આપવામાં આવતી અન્ય ઉપયોગી પદ્ધતિઓનો સમાવેશ થાય છે. `Stream` અને `StreamExt` હજી સુધી Rust ના સ્ટાન્ડર્ડ લાઇબ્રેરીનો ભાગ નથી, પરંતુ મોટાભાગના ઇકોસિસ્ટમ crates સમાન વ્યાખ્યાઓનો ઉપયોગ કરે છે.

સંકલક ભૂલનું નિવારણ એ `trpl::StreamExt` માટે `use` વિધાન ઉમેરવાનું છે, જેવો ઉલ્લેખ લિસ્ટિંગ ૧૭-૨૨ માં છે.

<Listing number="17-22" caption="Successfully using an iterator as the basis for a stream" file-name="src/main.rs">
```rust
{{#rustdoc_include ../listings/ch17-async-await/listing-17-22/src/main.rs:all}}
```
</Listing>
આ બધાં ઘટકો એકત્રિત થવાથી, આ કોડ આપણી ઇચ્છા મુજબ કાર્ય કરે છે! વળી, હવે કે `StreamExt` અવકાશમાં છે, તેથી અમે પુનરાવર્તકોની જેમ તેના તમામ ઉપયોગી પદ્ધતિઓનો ઉપયોગ કરી શકીએ છીએ.



[17-02-messages]: ch17-02-concurrency-with-async.html#message-passing
[iterator-trait]: ch13-02-iterators.html#the-iterator-trait-and-the-next-method
