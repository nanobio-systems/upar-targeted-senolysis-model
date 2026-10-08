## Mathematical Models ##

**Receptor Binding** <br>
$$
\frac{dB}{dt} = k_{on} \cdot N \cdot (R_{T} - B) - B \cdot (k_{off} + k_{int})
$$

**Endocytosis**
$$
\frac{dI}{dt} = k_{int} \cdot B - k_{clear} \cdot I
$$
$$
\frac{dI}{dt} = {V_{max} \cdot B}{K_{int} + B} - k_{clear} \cdot I
$$

**Intracellular Payload**
$$
\frac{dP}{dt} = k_{rel} \cdot I - k_{elim} \cdot P
$$
$$
\frac{dP}{dt} = (n \cdot t^{n-1}) \cdot I - k_{elim} \cdot P
$$

**Senescent-Cell Death**
$$
\frac{dS}{dt} = -k_{max} \cdot \frac{P^h}{EC_{50}^h + P^h} \cdot S