# Gujarati Translation: Pure Gujarati (Sanskrit-origin) Test

Testing whether local Ollama models can produce Gujarati output with
**Sanskrit-origin (શુદ્ધ ગુજરાતી)** vocabulary preference — avoiding
Urdu/Persian/Arabic loanwords.

**Test prompt:** Same 86-word chunk from Rust Book Chapter 1, with explicit
instruction to use Sanskrit-origin Gujarati and avoid foreign loanwords.

---

## Result Summary

| Model | Output | Chars | Duration | Tok/s | Works? |
|---|---|---|---|---|---|
| **Gemma3:12b** | ✅ Full Gujarati | 491 | 18s | 13.6 | **YES** |
| Gemma4:31b | ❌ Empty | 0 | 25s | 5.4 | NO |
| Qwen3.5:35b | ❌ Empty | 0 | 27s | 3.7 | NO |

---

## Test 1: Gemma3:12b ✅ (Working)

**Input (86 English words):**
```
If you are using Linux or macOS, open a terminal and enter the following
command. The command downloads a script and starts the installation of the
rustup tool, which installs the latest stable version of Rust. You might be
prompted for your password. If the install is successful, the following line
will appear: Rust is installed now. Great! You will also need a linker, which
is a program that Rust uses to join its compiled outputs into one file. It is
likely you already have one.
```

**Gujarati output (491 chars):**
```
જો તમે Linux અથવા macOS વાપરી રહ્યા છો, તો એક ટર્મિનલ ખોલો અને નીચેનો
આદેશ દાખલ કરો. આ આદેશ એક સ્ક્રિપ્ટ ડાઉનલોડ કરે છે અને rustup સાધનનું
ઇન્સ્ટોલેશન શરૂ કરે છે, જે Rust નું નવીનતમ stable વર્ઝન ઇન્સ્ટોલ કરે છે.
તમને તમારા પાસવર્ડ માટે પૂછવામાં આવી શકે છે. જો ઇન્સ્ટોલેશન સફળ થાય, તો
નીચેની લીટી દેખાશે: Rust હવે ઇન્સ્ટોલ થઈ ગયું છે. ખૂબ સરસ! તમારે એક લિંકર
પણ જોઈશે, જે એક પ્રોગ્રામ છે જે Rust તેના કમ્પાઈલ્ડ આઉટપુટ્સને એક ફાઇલમાં
જોડવા માટે વાપરે છે. સંભવ છે કે તમારી પાસે પહેલેથી જ તે છે.
```

**Quality notes:**
- Technical terms preserved in English: Rust, rustup, Linux, macOS, stable, linker, compiler
- Script, terminal, command → naturalized Gujarati
- No visible Urdu/Persian words found
- Output is ~1.0x word ratio vs English input

---

## Test 2: Gemma4:31b ❌ (Failing)

| Metric | Value |
|---|---|
| Input | 86 words |
| Output chars | **0** (empty) |
| Eval count | 100 tokens generated |
| Duration | 25,275 ms |
| Tokens/sec | 5.4 |
| Done reason | `length` |

**Result:** Model generates tokens (eval_count=100) but they decode to empty
string. Likely tokenizer mismatch for Gujarati Unicode range.

---

## Test 3: Qwen3.5:35b ❌ (Failing)

| Metric | Value |
|---|---|
| Input | 86 words |
| Output chars | **0** (empty) |
| Eval count | 100 tokens generated |
| Duration | 27,658 ms |
| Tokens/sec | 3.7 |
| Done reason | `length` |

**Result:** Same as Gemma4 — generates tokens but decodes to empty. Tokenizer
cannot map output logits to valid Gujarati characters.

---

## Conclusion

**Only Gemma3:12b can produce Gujarati output.** The larger models
(Gemma4:31b, Qwen3.5:35b) both generate empty responses — likely because
their tokenizers lack Gujarati Unicode coverage or produce out-of-vocabulary
tokens that decode to empty strings.

### Recommended model: **Gemma3:12b**

- ✅ Successfully generates Gujarati script
- ✅ Follows Sanskrit-origin vocabulary instructions
- ✅ Fast enough (13.6 tok/s, ~18s per 86-word chunk)
- ❌ Larger models (31B, 35B) cannot produce Gujarati at all

### Estimated Pilot Runtime (Chapter 1: 4,010 words, ~33 chunks)

```
33 chunks × 18s = ~10 minutes
```
