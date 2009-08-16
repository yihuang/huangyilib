function obj(){
    var b = 1;
    function s(xx){
        b = xx;
    }
    return {
        a: function(){
            s(2);
        return b;},
        b: function(){
            s(3);
            return b;
        },c:1,
        b:2
    };
}
