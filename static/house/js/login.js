$(document).ready(function () {
    $("#registe-btn").on('click', function () {
        $("#registeform").bootstrapValidator({
            // 图标 
            feedbackIcons: {
                valid: 'glyphicon glyphicon-ok',
                invalid: 'glyphicon glyphicon-remove',
                validating: 'glyphicon glyphicon-refresh'
            },
            // 表单校验的字段名
            fields: {
                name: {
                    validators: {
                        notEmpty: { // 非空校验
                            message: '用户名不能为空!'
                        },
                        stringLength: { // 长度校验
                            min: 6,
                            max: 10,
                            message: '用户名长度6到10个字符！'
                        },
                        regexp: { //正则校验
                            regexp: /^[a-zA-Z0-9_]+$/,
                            message: '用户名只能包含大写、小写、数字和下画线'
                        },
                        different: { // 比较是否不同，否的话校验不通过
                            field: 'password', // 和password字段比较
                            message: '用户名不能与密码相同'
                        }
                    }
                },
                password: {
                    validators: {
                        notEmpty: {
                            message: '密码不能为空!'
                        },
                        stringLength: {
                            min: 6,
                            max: 16,
                            message: '密码长度6到15个字符！'
                        },
                        different: {
                            field: 'name',
                            message: '密码不能与用户名相同'
                        }
                    }
                },
                confirmPassword: {
                    validators: {
                        notEmpty: {
                            message: '确认密码不能为空!'
                        },
                        stringLength: {
                            min: 6,
                            max: 16,
                            message: '确认密码长度6到15个字符！'
                        },
                        different: {
                            field: 'name',
                            message: '确认密码不能与用户名相同'
                        },
                        identical: { // 比较是否相同，否的话校验不通过
                            field: 'password', // 和password字段比较
                            message: '两次密码输入不一致'
                        }
                    }
                },
                email: {
                    validators: {
                        notEmpty: {
                            message: '邮箱不能为空!'
                        },
                        emailAddress: { 
                            message: '无效的邮箱地址'
                        }
                    }
                }
            }
        })
        //获取validator对象
        let validator = $("#registeform").data('bootstrapValidator');
        validator.isValid() //手动触发验证
        if (validator.isValid()) {
            console.log('------')
            console.log($("#registeform").serialize())
        }
    })

})