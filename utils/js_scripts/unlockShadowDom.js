(function () {
    const originalAttachShadow = Element.prototype.attachShadow;
    Element.prototype.attachShadow = function (init) {
        init.mode = 'open';
        return originalAttachShadow.call(this, init);
    };
    console.log(";)");
})();