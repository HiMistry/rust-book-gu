<!-- Old headings. Do not remove or links may break. -->
## Applying Concurrency with Async

આ વિભાગમાં, આપણે અસિંક (async) નો ઉપયોગ કરીને કેટલીક એવી એકરૂપતાની સમસ્યાઓ ઉકેલીશું જે આપણે પ્રકરણ ૧૬ માં થ્રેડો (threads) વડે ઉકેલી હતી. કારણ કે આપણે ત્યાં ઘણી મહત્વપૂર્ણ બાબતોની ચર્ચા કરી છે, આ વિભાગમાં આપણે થ્રેડો અને ફ્યુચર્સ (futures) વચ્ચે શું તફાવત છે તેના પર ધ્યાન કેન્દ્રિત કરીશું.

ઘણી પરિસ્થિતિઓમાં, અસિંક (async) નો ઉપયોગ કરીને એકરૂપતા સાથે કામ કરવા માટેના API, થ્રેડોનો ઉપયોગ કરવા માટેના API જેવા જ હોય છે. કેટલીક અન્ય પરિસ્થિતિઓમાં, તેઓ તદ્દન અલગ હોઈ શકે છે. ભલે API થ્રેડો અને અસિંક (async) વચ્ચે સમાન દેખાય, તેમ છતાં તેમની વર્તણૂક ઘણીવાર અલગ હોય છે—અને તેમની કામગીરીની લાક્ષણિકતાઓ લગભગ હંમેશાં અલગ હોય છે.

<!-- Old headings. Do not remove or links may break. -->
### Creating a New Task with `spawn_task`

અગાઉના "એક નવું થ્રેડ બનાવવું `spawn` સાથે" વિભાગમાં અમે બે અલગ થ્રેડ પર ગણતરી કરી હતી. ચાલો એ જ કાર્ય async નો ઉપયોગ કરીને કરીએ. `trpl` ક્રેટ `spawn_task` નામનું એક વિધેય (function) પૂરો પાડે છે જે `thread::spawn` API જેવું જ દેખાય છે, અને `sleep` નામનું વિધેય પણ આપે છે જે `thread::sleep` API નું async સંસ્કરણ છે. અમે આ બંનેનો ઉપયોગ કરીને ગણતરીનું ઉદાહરણ અમલમાં મૂકી શકીએ છીએ, જે યાદી 17-6 માં દર્શાવેલ છે.

<Listing number="17-6" caption="Creating a new task to print one thing while the main task prints something else" file-name="src/main.rs">
```rust
{{#rustdoc_include ../listings/ch17-async-await/listing-17-06/src/main.rs:all}}
```
</Listing>
As our starting point, we set up our `main` function with `trpl::block_on` so that our top-level function can be async. શરૂઆત તરીકે,

આપણે આપણું `main` વિધેય `trpl::block_on` સાથે ગોઠવીએ છીએ જેથી આપણું ઉચ્ચ સ્તરનું વિધેય અસિંક (async) બની શકે. નોંધ: આ પ્રકરણમાં હવેથી દરેક ઉદાહરણમાં આ ચોક્કસ આવરણ કોડ `trpl::block_on` સાથે `main` માં સમાવિષ્ટ હશે, તેથી આપણે ઘણીવાર તેને છોડી દઈશું જેમ કે આપણે `main` સાથે

કરીએ છીએ. તમારા કોડમાં તેને ઉમેરવાનું યાદ રાખો! પછી આપણે તે બ્લોકમાં બે લૂપ્સ લખીએ છીએ, જેમાં દરેક `trpl::sleep` કૉલ હોય છે, જે આગામી સંદેશ મોકલતા પહેલા અડધો સેકન્ડ (500 મિલીસેકન્ડ) રાહ જુએ છે. આપણે એક લૂપને `trpl::spawn_task` ના શરીરમાં મૂકીએ છીએ અને બીજાને ટોપ-લેવલ `for` લૂપમાં મૂકીએ છીએ. આપણે `sleep` કૉલ્સ પછી `await` પણ ઉમેરીએ છીએ.

આ કોડ થ્રેડ આધારિત અમલીકરણ જેવું જ વર્તન કરે છે— જેમાં એ હકીકતનો સમાવેશ થાય છે કે તમે જ્યારે તેને ચલાવો છો ત્યારે તમારા પોતાના ટર્મિનલમાં સંદેશાઓ અલગ ક્રમમાં દેખાઈ શકે છે:

<!-- Not extracting output because changes to this output aren't significant;
the changes are likely to be due to the threads running differently rather than
changes in the compiler -->
```text
hi number 1 from the second task!
hi number 1 from the first task!
hi number 2 from the first task!
hi number 2 from the second task!
hi number 3 from the first task!
hi number 3 from the second task!
hi number 4 from the first task!
hi number 4 from the second task!
hi number 5 from the first task!
```
આ આવૃત્તિ મુખ્ય અસિંક બ્લોકના શરીરમાં `for` લૂપ પૂર્ણ થતાં જ બંધ થઈ જાય છે, કારણ કે `spawn_task` દ્વારા શરૂ કરાયેલ કાર્ય `main` ફંક્શનના અંતિમ ભાગમાં સમાપ્ત થાય છે. જો તમે ઇચ્છો છો કે તે કાર્ય પૂર્ણ થાય ત્યાં સુધી ચાલુ રહે, તો તમારે પ્રથમ કાર્ય પૂર્ણ થવાની રાહ જોવા માટે જોઇન હેન્ડલનો ઉપયોગ કરવો પડશે. થ્રેડો સાથે, આપણે થ્રેડ પૂર્ણ ન થાય ત્યાં સુધી "બ્લોક" કરવા માટે `join` પદ્ધતિનો ઉપયોગ કર્યો હતો. લિસ્ટિંગ 17-7 માં, આપણે સમાન કાર્ય કરવા માટે `await` નો ઉપયોગ કરી શકીએ છીએ, કારણ કે ટાસ્ક હેન્ડલ પોતે જ ફ્યુચર છે. તેનું `Output` પ્રકાર એક `Result` છે, તેથી આપણે તેની રાહ જોયા પછી તેને અનવ્રેપ પણ કરીએ છીએ.

<Listing number="17-7" caption="Using `await` with a join handle to run a task to completion" file-name="src/main.rs">
```rust
{{#rustdoc_include ../listings/ch17-async-await/listing-17-07/src/main.rs:handle}}
```
</Listing>
આ સુધારેલું સંસ્કરણ બંને ચક્ર પૂર્ણ થાય ત્યાં સુધી ચાલે છે:

<!-- Not extracting output because changes to this output aren't significant;
the changes are likely to be due to the threads running differently rather than
changes in the compiler -->
```text
hi number 1 from the second task!
hi number 1 from the first task!
hi number 2 from the first task!
hi number 2 from the second task!
hi number 3 from the first task!
hi number 3 from the second task!
hi number 4 from the first task!
hi number 4 from the second task!
hi number 5 from the first task!
hi number 6 from the first task!
hi number 7 from the first task!
hi number 8 from the first task!
hi number 9 from the first task!
```
હાલમાં, એવું લાગે છે કે `async` અને થ્રેડ્સ આપણને સમાન પરિણામો આપે છે, માત્ર અલગ સિન્ટેક્સ સાથે: `join` હેન્ડલ પર કૉલ કરવાને બદલે `await` નો ઉપયોગ કરવો, અને `sleep` કૉલ્સની રાહ જોવી.

મોટો તફાવત એ છે કે આ કરવા માટે આપણે બીજા ઓપરેટિંગ સિસ્ટમ થ્રેડ બનાવવાની જરૂર નહોતી. હકીકતમાં, આપણને અહીં કોઈ કાર્ય શરૂ કરવાની પણ જરૂર નથી. કારણ કે `async` બ્લોક્સ અનામી ફ્યુચર્સમાં કમ્પાઇલ થાય છે, આપણે દરેક લૂપને `async` બ્લોકમાં મૂકી શકીએ છીએ અને રનટાઇમ બંનેને `trpl::join` ફંક્શનનો ઉપયોગ કરીને પૂર્ણ કરી શકે છે.

Waiting for All Threads to Finish અગાઉ પ્રકરણ ૧૬ નાં “સૂચિઓ પૂર્ણ થવાની રાહ” વિભાગમાં, અમે `JoinHandle` પ્રકાર પર `join` પદ્ધતિનો ઉપયોગ કેવી રીતે કરવો તે દર્શાવ્યું હતું, જે તમે `std::thread::spawn` કૉલ કરતી વખતે મેળવો છો. `trpl::join` કાર્ય સમાન છે, પરંતુ ભવિષ્ય માટે છે. જ્યારે તમે તેને બે ભવિષ્ય આપો છો, ત્યારે તે એક નવું ભવિષ્ય ઉત્પન્ન કરે છે જેનું પરિણામ એક ટ્યૂપલ હોય છે જેમાં દરેક ભવિષ્યના પરિણામો હોય છે, જે બંને પૂર્ણ થાય ત્યારે. આમ, સૂચિ ૧૭-૮ માં, અમે `trpl::join` નો ઉપયોગ `fut1` અને `fut2` બંને પૂર્ણ થાય તેની રાહ જોવા માટે કરીએ છીએ. અમે `fut1` અને `fut2` ની રાહ જોતા નથી, પરંતુ તેના બદલે `trpl::join` દ્વારા ઉત્પન્ન થયેલ નવા ભવિષ્યની રાહ જોઈએ છીએ. અમે આઉટપુટ અવગણીએ છીએ, કારણ કે તે માત્ર એક ટ્યૂપલ છે જેમાં બે એકમ મૂલ્યો હોય છે.

<Listing number="17-8" caption="Using `trpl::join` to await two anonymous futures" file-name="src/main.rs">
```rust
{{#rustdoc_include ../listings/ch17-async-await/listing-17-08/src/main.rs:join}}
```
</Listing>
જ્યારે આપણે આ ચલાવીએ છીએ, ત્યારે આપણે જોઈએ છીએ કે બંને ફ્યુચર્સ પૂર્ણ થાય છે:

<!-- Not extracting output because changes to this output aren't significant;
the changes are likely to be due to the threads running differently rather than
changes in the compiler -->
```text
hi number 1 from the first task!
hi number 1 from the second task!
hi number 2 from the first task!
hi number 2 from the second task!
hi number 3 from the first task!
hi number 3 from the second task!
hi number 4 from the first task!
hi number 4 from the second task!
hi number 5 from the first task!
hi number 6 from the first task!
hi number 7 from the first task!
hi number 8 from the first task!
hi number 9 from the first task!
```
હવે, તમે દરેક વખતે બરાબર એ જ ક્રમ જોશો, જે થ્રેડો અને `trpl::spawn_task` સાથે આપણે Listing 17-7 માં જે જોયું હતું તેનાથી ઘણું અલગ છે. આનું કારણ એ છે કે `trpl::join` વિધેય નિષ્પક્ષ (fair) છે, એટલે કે તે દરેક ભવિષ્ય (future)ને સમાન રીતે તપાસે છે, તેમની વચ્ચે ફેરબદલ કરે છે અને જો બીજું તૈયાર હોય તો એકને આગળ ન દોડવા દેતું નથી. થ્રેડો સાથે, ઓપરેટિંગ સિસ્ટમ નક્કી કરે છે કે કયો થ્રેડો તપાસવો અને તેને કેટલો સમય ચલાવવા દેવો. Async Rust સાથે, રનટાઇમ નક્કી કરે છે કે કયું કાર્ય (task) તપાસવું. (વ્યવહારમાં, વિગતો જટિલ બની જાય છે કારણ કે એક async રનટાઇમ સંસાધનની એકરૂપતા (concurrency)નું સંચાલન કરવાના ભાગ રૂપે ઓપરેટિંગ સિસ્ટમના થ્રેડોનો ઉપયોગ કરી શકે છે, તેથી નિષ્પક્ષતાની ખાતરી કરવી એ રનટાઇમ માટે વધુ મહેનત હોઈ શકે છે—પરંતુ તે હજી શક્ય છે!) રનટાઇમને કોઈપણ આપેલ ક્રિયા (operation) માટે નિષ્પક્ષતાની ખાતરી આપવાની જરૂર નથી, અને તેઓ ઘણીવાર વિવિધ API પ્રદાન કરે છે જેથી કરીને તમે નક્કી કરી શકો કે તમને નિષ્પક્ષતા જોઈએ છે કે નહીં.

આ પ્રયાસ કરો અને જુઓ કે તેઓ શું કરે છે: લૂપ્સમાંથી કોઈ

એક અથવા બંનેની `async` બ્લોક દૂર કરો. દરેક `async` બ્લોકને

વ્યાખ્યાયિત કર્યા પછી તરત જ અપેક્ષા રાખો.

માત્ર પ્રથમ લૂપને `async` બ્લોકમાં આવરી લો, અને બીજા લૂપના શરીર પછી પરિણામી ફ્યુચરની અપેક્ષા રાખો.

પરિચય આ એક પડકારરૂપ પ્રવૃત્તિ છે. દરેક કિસ્સામાં, કોડ ચલાવતા પહેલાં આઉટપુટ શું હશે તે જાણી શકશો?

<!-- Old headings. Do not remove or links may break. -->
### Sending Data Between Two Tasks Using Message Passing

ભવિષ્ય વચ્ચે માહિતી વહેંચવી એ પણ પરિચિત હશે: આપણે ફરીથી સંદેશા મોકલવાની પદ્ધતિનો ઉપયોગ કરીશું, પરંતુ આ વખતે પ્રકારો (types) અને વિધેયો (functions) ના અસમકાલીન (async) સંસ્કરણો સાથે. આપણે "થ્રેડ્સ વચ્ચે સંદેશા મોકલીને ડેટા ટ્રાન્સફર કરવો" પ્રકરણ ૧૬ ના વિભાગમાં જેટલો અલગ માર્ગ લીધો હતો, તેનાથી થોડો અલગ માર્ગ લઈશું, જેથી થ્રેડ-આધારિત અને ફ્યુચર્સ-આધારિત એકરૂપતા (concurrency) વચ્ચેના મુખ્ય તફાવતો દર્શાવી શકાય. લિસ્ટિંગ ૧૭-૯ માં, આપણે માત્ર એક જ અસમકાલીન બ્લોકથી શરૂઆત કરીશું— અલગ કાર્ય (task) શરૂ કર્યા વિના, જેમ કે આપણે પહેલાં એક અલગ થ્રેડ શરૂ કર્યો હતો.

<Listing number="17-9" caption="Creating an async channel and assigning the two halves to `tx` and `rx`" file-name="src/main.rs">
```rust
{{#rustdoc_include ../listings/ch17-async-await/listing-17-09/src/main.rs:channel}}
```
</Listing>
અહીં, આપણે `trpl::channel` નો ઉપયોગ કરીએ છીએ, જે બહુવિધ ઉત્પાદક અને એકલ ગ્રાહક ચેનલ API નું અસિંક્રૉનસ સંસ્કરણ છે જેનો આપણે પ્રકરણ ૧૬ માં થ્રેડો સાથે ઉપયોગ કર્યો હતો. API નું અસિંક્રૉનસ સંસ્કરણ થ્રેડ-આધારિત સંસ્કરણ કરતાં થોડું અલગ છે: તે અમૂટ (mutable) રીસીવર `rx` નો ઉપયોગ કરે છે, બદલે અવિભાજ્ય (immutable) રીસીવરનો, અને તેની `recv` પદ્ધતિ સીધી કિંમત ઉત્પન્ન કરવાને બદલે એક ફ્યુચર ઉત્પન્ન કરે છે જેને આપણે રાહ જોવાની જરૂર છે. હવે આપણે પ્રેષકથી ગ્રાહક સુધી સંદેશાઓ મોકલી શકીએ છીએ. નોંધ કરો કે આપણે અલગ થ્રેડ અથવા કાર્ય શરૂ કરવાની જરૂર નથી; આપણે માત્ર `rx.recv` કૉલની રાહ જોવાની જરૂર છે.

The synchronous `Receiver::recv` method in `std::mpsc::channel` blocks until it receives a message. The `trpl::Receiver::recv` method does not, because it is async. Instead of blocking, it hands control back to the runtime until either a message is received or the send side of the channel closes. By contrast, we don’t await the `send` call, because it doesn’t block. It doesn’t need to, because the channel we’re sending it into is unbounded.

Note: Because all of this async code runs in an async block in a `trpl::block_on` call, everything within it can avoid blocking. However, the code outside it will block on the `block_on` function returning. That’s the whole point of the `trpl::block_on` function: it lets you choose where to block on some set of async code, and thus where to transition between sync and async code.

આ ઉદાહરણમાં બે બાબતો ધ્યાન આપવા જેવી છે. પ્રથમ, સંદેશ તરત જ પહોંચશે. બીજું, ભલે આપણે અહીં future નો ઉપયોગ કરીએ છીએ, પરંતુ હજુ concurrency નથી.

યાદીમાં બધું ક્રમશઃ જ બનશે, જેમ કે જો futures સામેલ ન હોય તો થાત. ચાલો પ્રથમ ભાગને સંબોધિત કરીએ સંદેશોની શ્રેણી મોકલીને અને તેમની વચ્ચે થોડો સમય આરામ કરીને, જે Listing 17-10 માં દર્શાવેલ છે.

<!-- We cannot test this one because it never stops! -->
<Listing number="17-10" caption="Sending and receiving multiple messages over the async channel and sleeping with an `await` between each message" file-name="src/main.rs">
```rust
{{#rustdoc_include ../listings/ch17-async-await/listing-17-10/src/main.rs:many-messages}}
```
</Listing>
આ સંદેશાઓ મોકલવાની સાથે, આપણને તે પ્રાપ્ત કરવાની પણ જરૂર છે. આ કિસ્સામાં, કારણ કે આપણે જાણીએ છીએ કે કેટલા સંદેશાઓ આવી રહ્યા છે, તો આપણે `rx.recv().await` ને ચાર વખત બોલાવીને જાતે જ એ કરી શકીએ છીએ. વાસ્તવિક દુનિયામાં, જોકે, આપણે સામાન્ય રીતે અજ્ઞાત સંખ્યાના સંદેશાઓની રાહ જોઈશું, તેથી જ્યાં સુધી આપણને ખાતરી ન થાય કે કોઈ સંદેશો બાકી નથી, ત્યાં સુધી આપણે રાહ

જોતા રહેવું પડશે. Listing 16-10 લિસ્ટિંગ ૧૬-૧૦ માં, આપણે એક `for` લૂપનો ઉપયોગ કર્યો હતો જે સિંક્રોનસ ચેનલમાંથી મળેલા તમામ આઇટમ્સને પ્રોસેસ કરે છે. Rust પાસે હજી સુધી `for` લૂપનો ઉપયોગ કરીને એસિન્ક્રોનસ રીતે જનરેટ થયેલ આઇટમ્સની શ્રેણી સાથે કામ કરવાની રીત નથી, તેથી આપણે એક એવો લૂપ વાપરવાની જરૂર છે જે આપણે પહેલાં જોયો નથી: `while let` શરતી લૂપ. આ `if let` કન્સ્ટ્રક્ટનું લૂપ વર્ઝન છે જે આપણે પ્રકરણ ૬ માં "Concise Control Flow with `if let` and `let...else`" વિભાગમાં જોયો હતો. જ્યાં સુધી તે ઉલ્લેખિત કરેલ પેટર્ન મૂલ્ય સાથે મેળ ખાતો રહે ત્યાં સુધી લૂપ ચાલ્યા કરશે.

The `rx.recv` Call `rx.recv` આદેશ એક ફ્યુચર ઉત્પન્ન કરે છે, જેની આપણે રાહ જોઈએ છીએ. રનટાઈમ ફ્યુચરને તૈયાર થાય ત્યાં સુધી સ્થગિત કરશે. જ્યારે સંદેશો આવે છે, ત્યારે ફ્યુચર `Some(message)` સાથે જેટલી વાર સંદેશો આવશે તેટલી વાર ઉકેલાશે. જ્યારે ચેનલ બંધ થાય છે, ત્યારે કોઈપણ સંદેશો આવ્યો હોય કે ન હોય, ફ્યુચર `None` સાથે ઉકેલાશે, જે દર્શાવે છે કે હવે કોઈ મૂલ્યો નથી અને તેથી આપણે પોલિંગ બંધ કરવું જોઈએ—એટલે કે રાહ જોવાનું બંધ કરવું જોઈએ. The

`while let` Loop `while let` લૂપ આ બધું એકસાથે લાવે છે. જો `rx.recv().await` કૉલનું પરિણામ `Some(message)` હોય, તો આપણને સંદેશની ઍક્સેસ મળે છે અને આપણે તેનો ઉપયોગ લૂપના શરીરમાં કરી શકીએ છીએ, જેમ કે આપણે `if let` સાથે કરી શક્યા હોત. જો પરિણામ `None` હોય, તો લૂપ સમાપ્ત થાય છે. દરેક વખતે લૂપ પૂર્ણ થાય છે, ત્યારે તે ફરીથી અવેટ પોઈન્ટ પર આવે છે, તેથી રનટાઈમ તેને ફરીથી સ્થગિત કરે છે જ્યાં સુધી બીજો સંદેશ ન આવે.

હવે કોડ સફળતાપૂર્વક સંદેશાઓ મોકલે છે અને મેળવે છે. અભાગ્યવશાત, હજી થોડી સમસ્યાઓ બાકી છે. એક વાત તો એ છે કે સંદેશાઓ અડધો સેકન્ડના અંતરાલથી નથી આવતાં. તેઓ એકસાથે આવે છે, પ્રોગ્રામ શરૂ કર્યા પછી 2 સેકન્ડ (2,000 મિલીસેકન્ડ) જેટલા સમય બાદ. બીજી વાત એ છે કે આ પ્રોગ્રામ ક્યારેય બંધ થતો નથી! તેના બદલે, તે નવા સંદેશાઓની રાહ જુએ છે અનંતકાળ સુધી. તમારે તેને ctrl - C નો ઉપયોગ કરીને બંધ કરવું પડશે.

#### Code Within One Async Block Executes Linearly

ચાલો આપણે એ તપાસવાનું શરૂ કરીએ કે શા માટે સંદેશાઓ સંપૂર્ણ વિલંબ પછી એકસાથે આવે છે, દરેક વચ્ચે વિલંબ સાથે નહીં. આપેલ async બ્લોકમાં, કોડમાં `await` કીવર્ડ્સ જે ક્રમમાં દેખાય છે તે જ ક્રમમાં ચલાવવામાં આવે છે જ્યારે પ્રોગ્રામ ચાલે છે.

લિસ્ટિંગ 17-10 માં માત્ર એક જ async બ્લોક છે, તેથી તેમાં બધું જ રેખીય રીતે ચાલે છે. હજી પણ કોઈ સમન્વય (concurrency) નથી. બધા `tx.send` કૉલ્સ થાય છે, ત્યારબાદ બધા `trpl::sleep` કૉલ્સ અને તેમના સંલગ્ન અપેક્ષા બિંદુઓ (await points). ત્યારબાદ જ `while let` લૂપ `recv` કૉલ્સ પરના કોઈપણ `await` બિંદુઓમાંથી પસાર થઈ શકે છે.

આપણે જે વર્તન જોઈએ છે, જ્યાં દરેક સંદેશ વચ્ચે વિરામ આવે છે, તેના માટે આપણે `tx` અને `rx` ક્રિયાઓ તેમના પોતાના async બ્લોક્સમાં મૂકવાની જરૂર છે, જે Listing 17-11 માં દર્શાવેલ છે. પછી રનટાઈમ `trpl::join` નો ઉપયોગ કરીને દરેકને અલગથી ચલાવી શકે છે, બરાબર જેમ Listing 17-8 માં હતું. ફરીથી, આપણે `trpl::join` બોલાવવાનો પરિણામ આતુરતાથી જોવાની જરૂર છે, વ્યક્તિગત ફ્યુચર્સ નહીં. જો આપણે વ્યક્તિગત ફ્યુચર્સ ક્રમમાં આતુરતાથી જોયું તો આપણે માત્ર સિક્વન્સિયલ પ્રવાહમાં પાછા આવી જઈશું—બરાબર જે કરવાનું આપણે નથી ઈચ્છતા.

<!-- We cannot test this one because it never stops! -->
<Listing number="17-11" caption="Separating `send` and `recv` into their own `async` blocks and awaiting the futures for those blocks" file-name="src/main.rs">
```rust
{{#rustdoc_include ../listings/ch17-async-await/listing-17-11/src/main.rs:futures}}
```
</Listing>
ફેરફાર કરેલા કોડ સાથે યાદી ૧૭-૧૧ માં, સંદેશાઓ ૨ સેકન્ડ પછી એકસાથે છાપવાને બદલે, ૫૦૦ મિલિસેકન્ડના અંતરાલ પર છાપાય છે.

#### Moving Ownership Into an Async Block

જોકે, કાર્યક્રમ હજી પણ સમાપ્ત થતો નથી, કારણ કે `while let` લૂપ `trpl::join` સાથે કેવી રીતે ક્રિયાપ્રતિક્રિયા કરે છે.

`trpl::join` દ્વારા પરત કરવામાં આવેલું ભવિષ્ય (future) માત્ર ત્યારે જ પૂર્ણ થાય છે જ્યારે તેનામાં પસાર થયેલાં બંને ભવિષ્ય (futures) પૂર્ણ થાય છે.

`tx_fut` ભવિષ્ય અંતિમ સંદેશ `vals` માં મોકલ્યા પછી સૂઈ જવાનું પૂરું કરે એટલે પૂર્ણ થાય છે.

`rx_fut` ભવિષ્ય ત્યાં સુધી પૂર્ણ થશે નહીં જ્યાં સુધી `while let` લૂપ સમાપ્ત ન થાય.

`while let` લૂપ ત્યાં સુધી સમાપ્ત થશે નહીં જ્યાં સુધી `rx.recv` ની રાહ જોવા પર `None` ઉત્પન્ન ન થાય.

`rx.recv` ની રાહ જોવા પર `None` ત્યારે જ પાછું આવશે જ્યારે ચેનલનો બીજો છેડો બંધ કરવામાં આવે.

`tx` ચેનલ તો ત્યારે જ બંધ થશે જ્યારે આપણે `rx.close` કૉલ

કરીશું અથવા જ્યારે સેન્ડર ભાગ, `tx`, નાશ પામશે. આપણે `rx.close` ક્યાંય કૉલ કરતા નથી, અને `tx` ત્યારે જ નાશ પામશે જ્યારે સૌથી બહારનું async બ્લોક જે `trpl::block_on` ને

પસાર કરવામાં આવ્યું છે તે પૂર્ણ થશે. બ્લોક પૂર્ણ થઈ શકતું નથી કારણ કે તે `trpl::join` પૂર્ણ થવાની રાહ જોવામાં વ્યસ્ત છે, જે આપણને આ યાદીની શરૂઆતમાં પાછું લઈ જાય છે.

હાલમાં, એસિંક બ્લોક જ્યાં આપણે સંદેશાઓ મોકલીએ છીએ તે માત્ર `tx` ને ઉછીના લે છે કારણ કે સંદેશ મોકલવા માટે માલિકીની જરૂર નથી, પરંતુ જો આપણે `tx` ને તે એસિંક બ્લોકમાં ખસેડી શક્યા હોત, તો તે બ્લોક સમાપ્ત થતાં જ નાશ પામતું. પ્રકરણ ૧૩ માં "રેફરન્સ મેળવવું અથવા માલિકી ખસેડવી" વિભાગમાં, તમે `move` કીવર્ડનો ઉપયોગ ક્લોઝર્સ સાથે કેવી રીતે કરવો તે શીખ્યા હતા, અને પ્રકરણ ૧૬ માં "થ્રેડો સાથે `move` ક્લોઝર્સનો ઉપયોગ કરવો" વિભાગમાં ચર્ચા કર્યા મુજબ, થ્રેડો સાથે કામ કરતી વખતે આપણે ઘણીવાર ડેટાને ક્લોઝર્સમાં ખસેડવાની જરૂર પડે છે. એ જ મૂળભૂત ગતિશીલતા એસિંક બ્લોક્સ પર લાગુ થાય છે, તેથી `move` કીવર્ડ ક્લોઝર્સની જેમ એસિંક બ્લોક્સ સાથે પણ કામ કરે છે.

લિસ્ટિંગ ૧૭-૧૨ માં, આપણે સંદેશાઓ મોકલવા માટે વપરાયેલ બ્લોકને `async` થી `async move` માં બદલીએ છીએ.

<Listing number="17-12" caption="A revision of the code from Listing 17-11 that correctly shuts down when complete" file-name="src/main.rs">
```rust
{{#rustdoc_include ../listings/ch17-async-await/listing-17-12/src/main.rs:with-move}}
```
</Listing>
જ્યારે આપણે આ કોડના સંસ્કરણને ચલાવીએ છીએ, ત્યારે તે અંતિમ સંદેશ મોકલ્યા અને પ્રાપ્ત થયા પછી શાંતિથી બંધ થઈ જાય છે. હવે, ચાલો જોઈએ કે એક કરતાં વધુ ભવિષ્યમાંથી ડેટા મોકલવા માટે શું ફેરફાર કરવો જરૂરી છે.

#### Joining a Number of Futures with the `join!` Macro

આ અસિંક્રોન ચેનલ એક બહુવિધ ઉત્પાદક ચેનલ પણ છે, તેથી જો આપણે અનેક ફ્યુચર્સમાંથી સંદેશાઓ મોકલવા માંગતા હોઈએ તો આપણે `tx` પર `clone` કરી શકીએ છીએ, જે Listing 17-13 માં દર્શાવેલ છે.

<Listing number="17-13" caption="Using multiple producers with async blocks" file-name="src/main.rs">
```rust
{{#rustdoc_include ../listings/ch17-async-await/listing-17-13/src/main.rs:here}}
```
</Listing>
સૌ પ્રથમ, આપણે `tx` નકલ કરીએ છીએ, જેનાથી `tx1` પ્રથમ અસમન્વય બ્લોક બહાર બને છે. પછી, આપણે પહેલાની જેમ જ `tx1` ને તે બ્લોકમાં ખસેડીએ છીએ. ત્યારબાદ, આપણે મૂળ `tx` ને એક નવા અસમન્વય બ્લોકમાં ખસેડીએ છીએ, જ્યાં અમે થોડી ધીમી વિલંબ સાથે વધુ સંદેશાઓ મોકલીએ છીએ. આ નવો અસમન્વય બ્લોક સંદેશો મેળવવાના અસમન્વય બ્લોકની પછી મૂકવામાં આવ્યો છે, પરંતુ તે પહેલા પણ હોઈ શકતો હતો. મહત્વનું એ છે કે ભવિષ્યની રાહ ક્યાં જોવાઇ રહી છે, નહીં કે તેઓ ક્યારે બનાવવામાં આવ્યા હતા.

બંને અસિંક બ્લોક્સ સંદેશો મોકલવા માટે `async move` બ્લોક્સ હોવા જોઈએ જેથી `tx` અને `tx1` બંને તે બ્લોક્સ પૂર્ણ થતાં જ નાશ પામે. નહિંતર, આપણે એ જ અનંત ચક્રમાં પાછા આવીશું જે શરૂ થયું હતું.

અંતે, આપણે `trpl::join` થી `trpl::join!` માં બદલાઈએ છીએ જેથી વધારાના ફ્યુચરને સંભાળી શકાય: `join!` મેક્રો અસંખ્ય ફ્યુચર્સની રાહ જુએ છે જ્યાં આપણે કમ્પાઇલ સમયે ફ્યુચર્સની સંખ્યા જાણીએ છીએ. આપણે આ પ્રકરણમાં પછીથી અજ્ઞાત સંખ્યાના ફ્યુચર્સના સંગ્રહની રાહ જોવા વિશે ચર્ચા કરીશું.

હવે આપણે બંને મોકલતા ફ્યુચર્સના સંદેશાઓ જોઈએ છીએ, અને કારણ કે મોકલતા ફ્યુચર્સ સંદેશા મોકલ્યા પછી થોડા જુદા સમયગાળાનો ઉપયોગ કરે છે, તે સંદેશાઓ પણ તે જુદા જુદા અંતરાલો પર પ્રાપ્ત થાય છે:

<!-- Not extracting output because changes to this output aren't significant;
the changes are likely to be due to the threads running differently rather than
changes in the compiler -->
```text
received 'hi'
received 'more'
received 'from'
received 'the'
received 'messages'
received 'future'
received 'for'
received 'you'
```
આપણે જોયું છે કે સંદેશાવ્યવહારનો ઉપયોગ કરીને ભવિષ્ય વચ્ચે ડેટા કેવી રીતે મોકલવો, એસિંક બ્લોકમાં કોડ ક્રમશઃ કેવી રીતે ચાલે છે, એસિંક બ્લોકમાં માલિકી કેવી રીતે ખસેડવી અને બહુવિધ ભવિષ્યને કેવી રીતે જોડવું. હવે પછી, આપણે ચર્ચા કરીશું કે રનટાઇમને ક્યારે અને શા માટે અન્ય કાર્ય પર સ્વિચ કરવાની મંજૂરી આપવી જોઈએ.



[thread-spawn]: ch16-01-threads.html#creating-a-new-thread-with-spawn
[join-handles]: ch16-01-threads.html#waiting-for-all-threads-to-finish
[message-passing-threads]: ch16-02-message-passing.html
[if-let]: ch06-03-if-let.html
[capture-or-move]: ch13-01-closures.html#capturing-references-or-moving-ownership
[move-threads]: ch16-01-threads.html#using-move-closures-with-threads
