## Comments

બધા જ પ્રોગ્રામરો પ્રયત્ન કરે છે કે તેમની કોડ સરળતાથી સમજી શકાય, પરંતુ કેટલીક વાર વધારાની સમજૂતી જરૂરી બને છે. આવી પરિસ્થિતિઓમાં, પ્રોગ્રામરો તેમના સ્રોત કોડમાં ટિપ્પણીઓ મૂકે છે, જે કમ્પાઇલર અવગણે છે, પરંતુ સ્રોત કોડ વાંચતા લોકો માટે ઉપયોગી થઈ શકે છે.

અહીં એક સરળ ટિપ્પણીનું ઉદાહરણ છે:

// hello, world
Rust માં ટિપ્પણી શૈલી Rust માં, સામાન્ય રીતે વપરાતી ટિપ્પણી શૈલી બે ધાતુવાળી લીટીઓ (slashes) થી શરૂ થાય છે, અને ટિપ્પણી લીટીના અંત સુધી ચાલુ રહે છે. જો ટિપ્પણી એક કરતાં વધુ લીટી સુધી ફેલાય, તો તમારે દરેક લીટી પર `//` ઉમેરવાની જરૂર પડશે, જેમ કે આ:

// So we're doing something complicated here, long enough that we need
// multiple lines of comments to do it! Whew! Hopefully, this comment will
// explain what's going on.
ટિપ્પણીઓ કોડ ધરાવતા લીટીઓના અંતે પણ મૂકી શકાય છે:

ફાઈલનામ: src/main.rs

{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-24-comments-end-of-line/src/main.rs}}
પરંતુ તમે સામાન્ય રીતે તેમને આ ફોર્મેટમાં જોઈ શકશો, જ્યાં ટિપ્પણી કોડની ઉપર અલગ લાઈનમાં હોય:

ફાઈલનામ: src/main.rs

{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-25-comments-above-line/src/main.rs}}
Rustમાં અન્ય પ્રકારની ટીકા પણ છે, જે માહિતી ટીકા છે, જેના વિશે આપણે પ્રકરણ ૧૪ ના “Crates.io પર Crate પ્રકાશિત કરવું” વિભાગમાં ચર્ચા કરીશું.

