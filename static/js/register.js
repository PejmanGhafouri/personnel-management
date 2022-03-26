var current_fs, next_fs, previous_fs; //fieldsets
var left, opacity, scale; //fieldset properties which we will animate
var animating; //flag to prevent quick multi-click glitches


$("#id_profiles-0-martial_status").on("change", function () {
    $(".showMarried").hide();
    $("#" + $(this).val()).slideDown(1000);

})

$("#add-child").click(function () {
    $(".showChild").hide();
    $("#child" + $(this).val()).slideDown(1000);
    $("#add-child").css('display', 'none');
})

$(".next").click(function () {
    if (animating) return false;
    animating = true;

    current_fs = $(this).parent();
    next_fs = $(this).parent().next();

    //activate next step on progressbar using the index of next_fs
    $("#progressbar li").eq($("fieldset").index(next_fs)).addClass("active");

    //show the next fieldset
    next_fs.show();
    //hide the current fieldset with style
    current_fs.animate({opacity: 0}, {
        step: function (now, mx) {
            //as the opacity of current_fs reduces to 0 - stored in "now"
            //1. scale current_fs down to 80%
            scale = 1 - (1 - now) * 0.2;
            //2. bring next_fs from the right(50%)
            left = (now * 50) + "%";
            //3. increase opacity of next_fs to 1 as it moves in
            opacity = 1 - now;
            current_fs.css({
                'transform': 'scale(' + scale + ')',
                'position': 'absolute'
            });
            next_fs.css({'left': left, 'opacity': opacity});
        },
        duration: 800,
        complete: function () {
            current_fs.hide();
            animating = false;
        },
        //this comes from the custom easing plugin
        easing: 'easeInOutBack'
    });
});

$(".previous").click(function () {
    if (animating) return false;
    animating = true;

    current_fs = $(this).parent();
    previous_fs = $(this).parent().prev();

    //de-activate current step on progressbar
    $("#progressbar li").eq($("fieldset").index(current_fs)).removeClass("active");

    //show the previous fieldset
    previous_fs.show();
    //hide the current fieldset with style
    current_fs.animate({opacity: 0}, {
        step: function (now, mx) {
            //as the opacity of current_fs reduces to 0 - stored in "now"
            //1. scale previous_fs from 80% to 100%
            scale = 0.8 + (1 - now) * 0.2;
            //2. take current_fs to the right(50%) - from 0%
            left = ((1 - now) * 50) + "%";
            //3. increase opacity of previous_fs to 1 as it moves in
            opacity = 1 - now;
            current_fs.css({'left': left});
            previous_fs.css({'transform': 'scale(' + scale + ')', 'opacity': opacity});
        },
        duration: 800,
        complete: function () {
            current_fs.hide();
            animating = false;
        },
        //this comes from the custom easing plugin
        easing: 'easeInOutBack'
    });
});

$(".submit").click(function () {
    return false;
})

function sunnyweb_check_number() {
    var cardnumber = document.getElementById("cardnumber").value;
    document.getElementById('card_er').style.display = 'none';

    function validateCard(code) {
        var L = code.length;
        if (L < 16 || parseInt(code.substr(1, 10), 10) == 0 || parseInt(code.substr(10, 6), 10) == 0) return false;
        var c = parseInt(code.substr(15, 1), 10);
        var s = 0;
        var k, d;
        for (var i = 0; i < 16; i++) {
            k = (i % 2 == 0) ? 2 : 1;
            d = parseInt(code.substr(i, 1), 10) * k;
            s += (d > 9) ? d - 9 : d;
        }
        return ((s % 10) == 0);
    }

    if (validateCard(cardnumber) === false) document.getElementById('card_er').style.display = 'block';
    var number = cardnumber.substring(6, -16);
    var imgToSwap = document.getElementById("img0");

    if (number === '603799') {
        imgToSwap.src = "../img/bank-iran/meli.png";
    }
    if (number === '589210') {
        imgToSwap.src = "../img/bank-iran/sepah.png";
    }
    if (number === '627961') {
        imgToSwap.src = "../img/bank-iran/sanatmadan.png";
    }
    if (number === '603770') {
        imgToSwap.src = "../img/bank-iran/keshavarsi.png";
    }
    if (number === '628023') {
        imgToSwap.src = "../img/bank-iran/maskan.png";
    }
    if (number === '627760') {
        imgToSwap.src = "../img/bank-iran/postbank.png";
    }
    if (number === '502908') {
        imgToSwap.src = "../img/bank-iran/tosehe.png";
    }
    if (number === '627412') {
        imgToSwap.src = "../img/bank-iran/eghtesad.png";
    }
    if (number === '622106') {
        imgToSwap.src = "../img/bank-iran/parsian.png";
    }
    if (number === '502229') {
        imgToSwap.src = "../img/bank-iran/pasargad.png";
    }
    if (number === '627488') {
        imgToSwap.src = "../img/bank-iran/karafarin.png";
    }
    if (number === '621986') {
        imgToSwap.src = "../img/bank-iran/saman.png";
    }
    if (number === '639346') {
        imgToSwap.src = "../img/bank-iran/sina.png";
    }
    if (number === '639607') {
        imgToSwap.src = "../img/bank-iran/sarmaye.png";
    }
    if (number === '502806') {
        imgToSwap.src = "../img/bank-iran/shahr.png";
    }
    if (number === '502938') {
        imgToSwap.src = "../img/bank-iran/day.png";
    }
    if (number === '603769') {
        imgToSwap.src = "../img/bank-iran/saderat.png";
    }
    if (number === '610433') {
        imgToSwap.src = "../img/bank-iran/mellat.png";
    }
    if (number === '627353') {
        imgToSwap.src = "../img/bank-iran/tejarat.png";
    }
    if (number === '589463') {
        imgToSwap.src = "../img/bank-iran/refah.png";
    }
    if (number === '627381') {
        imgToSwap.src = "../img/bank-iran/ansar.png";
    }
    if (number === '639370') {
        imgToSwap.src = "../img/bank-iran/mehreqtesad.png";
    }
    if (number === '639599') {
        imgToSwap.src = "../img/bank-iran/ghavamin.png";
    }
    if (number === '504172') {
        imgToSwap.src = "../img/bank-iran/resalat.png";
    }
}

// bank-extra-button
function updateElementIndex(el, prefix, ndx
) {
    let id_regex = new RegExp('(' + prefix + '-\\d+)');
    let replacement = prefix + '-' + ndx;
    if ($(el).attr("for")) $(el).attr("for", $(el).attr("for").replace(id_regex, replacement));
    if (el.id) el.id = el.id.replace(id_regex, replacement);
    if (el.name) el.name = el.name.replace(id_regex, replacement);
}

function cloneMore(selector, prefix
) {
    let newElement = $(selector).clone(true);
    let total = $('#id_' + prefix + '-TOTAL_FORMS').val();
    newElement.find(':input:not([type=button]):not([type=submit]):not([type=reset])').each(function () {
        let name = $(this).attr('name').replace('-' + (total - 1) + '-', '-' + total + '-');
        let id = 'id_' + name;
        $(this).attr({'name': name, 'id': id}).val('').removeAttr('checked');
    });
    newElement.find('label').each(function () {
        let forValue = $(this).attr('for');
        if (forValue) {
            forValue = forValue.replace('-' + (total - 1) + '-', '-' + total + '-');
            $(this).attr({'for': forValue});
        }
    });
    total++;
    $('#id_' + prefix + '-TOTAL_FORMS').val(total);
    $(selector).after(newElement);
    let conditionRow = $('.bank-row:not(:last)');
    conditionRow.find('.btn.add-bank-form-row')
    return false;
}

$(document).on('click', '.add-bank-form-row', function (e) {
    e.preventDefault();
    cloneMore('.bank-row:last', 'form');
    return false;
})

// education-extra-button
function updateElementIndex(el, prefix, ndx
) {
    let id_regex = new RegExp('(' + prefix + '-\\d+)');
    let replacement = prefix + '-' + ndx;
    if ($(el).attr("for")) $(el).attr("for", $(el).attr("for").replace(id_regex, replacement));
    if (el.id) el.id = el.id.replace(id_regex, replacement);
    if (el.name) el.name = el.name.replace(id_regex, replacement);
}

function cloneMore(selector, prefix
) {
    let newElement = $(selector).clone(true);
    let total = $('#id_' + prefix + '-TOTAL_FORMS').val();
    newElement.find(':input:not([type=button]):not([type=submit]):not([type=reset])').each(function () {
        let name = $(this).attr('name').replace('-' + (total - 1) + '-', '-' + total + '-');
        let id = 'id_' + name;
        $(this).attr({'name': name, 'id': id}).val('').removeAttr('checked');
    });
    newElement.find('label').each(function () {
        let forValue = $(this).attr('for');
        if (forValue) {
            forValue = forValue.replace('-' + (total - 1) + '-', '-' + total + '-');
            $(this).attr({'for': forValue});
        }
    });
    total++;
    $('#id_' + prefix + '-TOTAL_FORMS').val(total);
    $(selector).after(newElement);
    let conditionRow = $('.education-row:not(:last)');
    conditionRow.find('.btn.add-education-form-row')
    return false;
}

$(document).on('click', '.add-education-form-row', function (e) {
    e.preventDefault();
    cloneMore('.education-row:last', 'form');
    return false;
})


// spouse-extra-button
function updateElementIndex(el, prefix, ndx
) {
    let id_regex = new RegExp('(' + prefix + '-\\d+)');
    let replacement = prefix + '-' + ndx;
    if ($(el).attr("for")) $(el).attr("for", $(el).attr("for").replace(id_regex, replacement));
    if (el.id) el.id = el.id.replace(id_regex, replacement);
    if (el.name) el.name = el.name.replace(id_regex, replacement);
}

function cloneMore(selector, prefix
) {
    let newElement = $(selector).clone(true);
    let total = $('#id_' + prefix + '-TOTAL_FORMS').val();
    newElement.find(':input:not([type=button]):not([type=submit]):not([type=reset])').each(function () {
        let name = $(this).attr('name').replace('-' + (total - 1) + '-', '-' + total + '-');
        let id = 'id_' + name;
        $(this).attr({'name': name, 'id': id}).val('').removeAttr('checked');
    });
    newElement.find('label').each(function () {
        let forValue = $(this).attr('for');
        if (forValue) {
            forValue = forValue.replace('-' + (total - 1) + '-', '-' + total + '-');
            $(this).attr({'for': forValue});
        }
    });
    total++;
    $('#id_' + prefix + '-TOTAL_FORMS').val(total);
    $(selector).after(newElement);
    let conditionRow = $('.spouse-row:not(:last)');
    conditionRow.find('.btn.add-spouse-form-row')
    return false;
}

$(document).on('click', '.add-spouse-form-row', function (e) {
    e.preventDefault();
    cloneMore('.spouse-row:last', 'form');
    return false;
})


// child-extra-button
function updateElementIndex(el, prefix, ndx
) {
    let id_regex = new RegExp('(' + prefix + '-\\d+)');
    let replacement = prefix + '-' + ndx;
    if ($(el).attr("for")) $(el).attr("for", $(el).attr("for").replace(id_regex, replacement));
    if (el.id) el.id = el.id.replace(id_regex, replacement);
    if (el.name) el.name = el.name.replace(id_regex, replacement);
}

function cloneMore(selector, prefix
) {
    let newElement = $(selector).clone(true);
    let total = $('#id_' + prefix + '-TOTAL_FORMS').val();
    newElement.find(':input:not([type=button]):not([type=submit]):not([type=reset])').each(function () {
        let name = $(this).attr('name').replace('-' + (total - 1) + '-', '-' + total + '-');
        let id = 'id_' + name;
        $(this).attr({'name': name, 'id': id}).val('').removeAttr('checked');
    });
    newElement.find('label').each(function () {
        let forValue = $(this).attr('for');
        if (forValue) {
            forValue = forValue.replace('-' + (total - 1) + '-', '-' + total + '-');
            $(this).attr({'for': forValue});
        }
    });
    total++;
    $('#id_' + prefix + '-TOTAL_FORMS').val(total);
    $(selector).after(newElement);
    let conditionRow = $('.child-row:not(:last)');
    conditionRow.find('.btn.add-child-form-row')
    return false;
}

$(document).on('click', '.add-child-form-row', function (e) {
    e.preventDefault();
    cloneMore('.child-row:last', 'form');
    return false;
})
