(function () {
    "use strict";

    if (window.location.protocol !== "https:" ||
        window.location.hostname !== "peacock-rt.readthedocs.io") {
        return;
    }

    var script = document.createElement("script");
    script.async = true;
    script.src = "https://gc.zgo.at/count.js";
    script.setAttribute("data-goatcounter", "https://lzhastro-peacock.goatcounter.com/count");
    document.head.appendChild(script);
}());
