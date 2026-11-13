(function () {
    "use strict";

    if (window.location.protocol !== "https:" ||
        window.location.hostname !== "peacock-rt.readthedocs.io") {
        return;
    }

    var path = window.location.pathname
        .replace(/^\/en\/latest(?:\/|$)/, "/")
        .replace(/\/index\.html$/, "/")
        .replace(/\.html$/, "")
        .replace(/\/+$/, "") || "/";

    var script = document.createElement("script");
    script.async = true;
    script.src = "https://gc.zgo.at/count.js";
    script.setAttribute("data-goatcounter", "https://lzhastro-peacock.goatcounter.com/count");
    script.setAttribute("data-goatcounter-settings", JSON.stringify({path: path}));
    document.head.appendChild(script);
}());
