$(document).ready(function () {
    // 确保模态框正常工作
    $(document).on('click', '[data-toggle="modal"]', function(e) {
        e.preventDefault();
        var target = $(this).data('target');
        $(target).modal('show');
    });
    
    // 模态框隐藏时清理
    $('.modal').on('hidden.bs.modal', function () {
        $(this).find('form')[0].reset();
        // 清除验证状态
        var validatorObj = $(this).find('form').data('bootstrapValidator');
        if (validatorObj && typeof validatorObj.destroy === 'function') {
            validatorObj.destroy();
            $(this).find('form').data('bootstrapValidator', null);
        }
    });

    // 注册
    $('#registe-btn').on('click', function () {
        $('#registeform').bootstrapValidator({
            message: 'This value is not valid',
            fields: {
                username: {
                    message: 'The username is not valid',
                    validators: {
                        notEmpty: {
                            message: '用户名不能为空'
                        },
                        stringLength: {
                            min: 6,
                            max: 15,
                            message: '用户名长度必须在6到15位之间'
                        },
                        regexp: {
                            regexp: /^[a-zA-Z0-9_\.]+$/,
                            message: '用户名只能包含大写、小写、数字和下画线'
                        },
                        different: {
                            field: 'password',
                            message: '用户名不能与密码相同'
                        }
                    }
                },
                email: {
                    validators: {
                        notEmpty: {
                            message: '邮箱不能为空'
                        },
                        emailAddress: {
                            message: '无效的邮箱地址'
                        }
                    }
                },
                password: {
                    validators: {
                        notEmpty: {
                            message: '密码不能为空'
                        },
                        identical: {
                            field: 'confirmPassword',
                            message: '与确认密码不一致'
                        },
                        different: {
                            field: 'username',
                            message: '密码不能与用户名相同'
                        }
                    }
                },
                confirmPassword: {
                    validators: {
                        notEmpty: {
                            message: '确认密码不能为空'
                        },
                        identical: {
                            field: 'password',
                            message: '与密码不一致'
                        },
                        different: {
                            field: 'username',
                            message: '确认密码不能与用户名相同'
                        }
                    }
                }
            }
        });
        var validator = $('#registeform').data("bootstrapValidator"); //获取validator对象
        validator.validate(); //手动触发验证
        if (validator.isValid()) { //通过验证
            $.ajax({
                type: 'post',
                url: '/register',
                data: $('#registeform').serialize(),
                dataType: 'json',
                success: function (result) {
                    if (result['valid'] == '0') {
                        alert(result['msg'])
                        // 清空注册表单
                        $('#registeform')[0].reset();
                        // 清除验证状态
                        var validatorObj = $("#registeform").data('bootstrapValidator');
                        if (validatorObj && typeof validatorObj.destroy === 'function') {
                            validatorObj.destroy();
                            $('#registeform').data('bootstrapValidator', null);
                        }
                    } else {
                        alert("注册成功！");
                        // 注册成功后,跳转首页页面,自动点击登录按钮
                        $('#register').modal('hide');  // 隐藏注册弹窗
                        // 等待模态框完全隐藏后再显示登录模态框
                        setTimeout(function() {
                            $('#login').modal('show');  // 显示登录弹窗
                        });
                    }
                },

            })
        }
    });

    // 登录
    $('#login-btn').on('click', function () {
        $('#loginform').bootstrapValidator({
            message: 'This value is not valid',
            fields: {
                username: {
                    message: 'The username is not valid',
                    validators: {
                        notEmpty: {
                            message: '用户名不能为空'
                        },
                        stringLength: {
                            min: 6,
                            max: 15,
                            message: '用户名长度必须在6到15位之间'
                        },
                        regexp: {
                            regexp: /^[a-zA-Z0-9_\.]+$/,
                            message: '用户名只能包含大写、小写、数字和下划线'
                        }
                    }
                },
                password: {
                    validators: {
                        notEmpty: {
                            message: '密码不能为空'
                        },
                        different: {
                            field: 'username',
                            message: '密码不能与用户名相同'
                        }
                    }
                }
            }
        }); //验证配置
        var validator = $('#loginform').data("bootstrapValidator"); //获取validator对象
        validator.validate(); //手动触发验证
        if (validator.isValid()) { //通过验证
            $.ajax({
                type: 'post',
                url: '/login',
                data: $('#loginform').serialize(),
                dataType: 'json',
                success: function (result) {
                    if (result['valid'] == '0') {
                        alert(result['msg'])
                        var validatorObj = $("#loginform").data('bootstrapValidator');
                        if (validatorObj && typeof validatorObj.destroy === 'function') {
                            validatorObj.destroy();
                            $('#loginform').data('bootstrapValidator', null);
                        }
                    } else {
                        alert("登录成功！");
                        window.location.replace("/user/" + result['msg']);
                    }
                },

            })
        }
    });

    // 退出登录

    $('#logout').on('click', function (e) {
        e.preventDefault();  // 阻止默认行为
        console.log("退出登录按钮被点击");
        $.ajax({
            url: '/logout',
            type: 'get', 
            success: function(res){
                if (res.valid == '1') {
                    alert(res.msg);
                    window.location.href = '/';
                } else {
                    alert(res.msg);
                }
            },
            error: function(xhr, status, error) {
                console.log("请求失败:", error);
                alert("退出失败，请重试");
            }
        });
    });
});