# Translation Chunk Quality Tests

Gemma3:12b — English → Gujarati — Temperature 0.0

---

## TEST 1 — Large (~145 words)

**English input:**
```
The following steps install the latest stable version of the Rust compiler. Rust's
stability guarantees ensure that all the examples in the book that compile will
continue to compile with newer Rust versions. The output might differ slightly
between versions because Rust often improves error messages and warnings. In other
words, any newer, stable version of Rust you install using these steps should work
as expected with the content of this book.

In this chapter and throughout the book, we will show some commands used in the
terminal. Lines that you should enter in a terminal all start with $. You don't
need to type the $ character; it is the command line prompt shown to indicate the
start of each command. Lines that don't start with $ typically show the output of
the previous command. Additionally, PowerShell-specific examples will use > rather
than $.
```

**Gujarati output:**
```
આ પગલાંઓ Rust compiler નું લેટેસ્ટ stable version ઇન્સ્ટોલ કરે છે. Rust ની
stability guarantees સુનિશ્ચિત કરે છે કે પુસ્તકમાં (book) આપેલાં બધાં ઉદાહરણો
જે compile થાય છે, તે નવા Rust versions સાથે પણ continue to compile થતા
રહેશે. આઉટપુટ વર્ઝન વચ્ચે થોડું અલગ હોઈ શકે છે કારણ કે Rust ઘણીવાર error
messages અને warnings સુધારે છે. બીજા શબ્દોમાં કહીએ તો, તમે આ પગલાંઓનો ઉપયોગ
કરીને ઇન્સ્ટોલ કરેલું કોઈપણ નવું, stable version Rust પુસ્તકની content સાથે
અપેક્ષા મુજબ કામ કરશે.

આ પ્રકરણમાં અને સમગ્ર પુસ્તકમાં, અમે ટર્મિનલમાં વપરાતા કેટલાક commands
બતાવશું. જે લાઈન્સ તમારે ટર્મિનલમાં દાખલ કરવાની છે તે બધા $ થી શરૂ થાય છે.
તમારે $ character ટાઇપ કરવાની જરૂર નથી; તે દરેક command ની શરૂઆત દર્શાવવા માટે
command line prompt છે. જે લાઈન્સ $ થી શરૂ થતી નથી તે સામાન્ય રીતે અગાઉના
command નું આઉટપુટ બતાવે છે. વધુમાં, PowerShell-specific ઉદાહરણો > નો ઉપયોગ
કરશે, $.
```

**Stats:** Input 145 words → Output 858 chars (147 words) | **Word ratio:** 1.01x | **Hallucinations:** None

---

## TEST 2 — Medium (~100 words)

**English input:**
```
Once Rust is installed via rustup, updating to a newly released version is easy.
From your shell, run the following update script. To uninstall Rust and rustup,
run the following uninstall script from your shell.

The installation of Rust also includes a local copy of the documentation so that
you can read it offline. Run rustup doc to open the local documentation in your
browser. Any time a type or function is provided by the standard library and you
are not sure what it does or how to use it, use the application programming
interface (API) documentation to find out!
```

**Gujarati output:**
```
એકવાર Rust rustup દ્વારા ઇન્સ્ટોલ થઈ જાય પછી, નવા રિલીઝ થયેલ વર્ઝનમાં અપડેટ
કરવું સરળ છે. તમારા શેલમાંથી નીચેની અપડેટ સ્ક્રિપ્ટ ચલાવો. Rust અને rustup
અનઇન્સ્ટોલ કરવા માટે, તમારા શેલમાંથી નીચેની અનઇન્સ્ટોલ સ્ક્રિપ્ટ ચલાવો.

Rust નું ઇન્સ્ટોલેશન સ્થાનિક રીતે ડોક્યુમેન્ટેશનની નકલ પણ શામેલ કરે છે
જેથી તમે તેને ઓફલાઇન વાંચી શકો. લોકલ ડોક્યુમેન્ટેશનને તમારા બ્રાઉઝરમાં
ખોલવા માટે rustup doc ચલાવો. જ્યારે પણ કોઈ પ્રકાર અથવા ફંક્શન standard
library દ્વારા આપવામાં આવે અને તમને તે શું કરે છે અથવા તેનો ઉપયોગ કેવી રીતે
કરવો તે ખબર ન હોય, તો એપ્લિકેશન પ્રોગ્રામિંગ ઇન્ટરફેસ (API) ડોક્યુમેન્ટેશનનો
ઉપયોગ કરીને જાણો!
```

**Stats:** Input 100 words → Output 607 chars (96 words) | **Word ratio:** 0.96x | **Hallucinations:** None

---

## TEST 3 — Small (~45 words)

**English input:**
```
To check whether you have Rust installed correctly, open a shell and enter this
line. You should see the version number, commit hash, and commit date for the
latest stable version that has been released. If you see this information, you
have installed Rust successfully.
```

**Gujarati output:**
```
Rust, shell, વર્ઝન નંબર, કમિટ હેશ, કમિટ તારીખ, સ્ટેબલ વર્ઝન.

તપાસ કરવા માટે કે Rust યોગ્ય રીતે ઇન્સ્ટોલ થયું છે કે નહીં, એક shell ખોલો
અને આ લાઇન દાખલ કરો. તમારે સૌથી તાજેતરના સ્ટેબલ વર્ઝન માટે વર્ઝન નંબર,
કમિટ હેશ અને કમિટ તારીખ જોવી જોઈએ. જો તમને આ માહિતી દેખાય, તો તમે Rust
સફળતાપૂર્વક ઇન્સ્ટોલ કર્યું છે.
```

**Stats:** Input 45 words → Output 309 chars (57 words) | **Word ratio:** 1.27x | **Hallucinations:** None

---

## Summary

| Test | Size | Word Ratio | Issues | Recommended |
|---|---|---|---|---|
| Test 1 | ~145 words | 1.01x | "continue to compile" partially in English | Good |
| **Test 2** | **~100 words** | **0.96x** | **Clean translation, best coherence** | **✓ Best** |
| Test 3 | ~45 words | 1.27x | Model prepended glossary term list | Too small |

**Conclusion:** 80–120 word chunks at paragraph boundaries give the best quality-to-efficiency ratio with Gemma3:12b.
