// 标签页切换
$(".nav-tabs li").click(function () {
    let status = $(this).hasClass("chanle1")
    if (status) {
        $(".user-info").show();
        $(".collection").hide()
        $(".chanle1").addClass("active")
    }
    else {
        $(".user-info").hide();
        $(".collection").show()
    }
    $(this).addClass("active").siblings().removeClass("active")
})

// 获取原始表单数据
var originalData = $('#profile-form').serialize();
var originalUsername = $('#username').val();

// 个人信息表单提交
$('#profile-form').submit(function(e) {
    e.preventDefault();
    console.log('提交按钮被点击');
    
    // 获取表单数据
    var username = $('#username').val().trim();
    var addr = $('#addr').val().trim();
    var password = $('#password').val();
    var email = $('#email').val().trim();
    
    // 自定义验证
    var isValid = true;
    var errorMessage = '';
    
    // 验证用户名
    if (!username) {
        isValid = false;
        errorMessage = '用户名不能为空';
    }
    
    // 验证邮箱
    if (!email) {
        isValid = false;
        errorMessage = '邮箱不能为空';
    } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
        isValid = false;
        errorMessage = '邮箱格式不正确';
    }
    
    if (!isValid) {
        alert(errorMessage);
        return;
    }
    
    // 检查是否有修改
    var hasChanges = false;
    
    // 检查用户名是否修改
    if (username !== originalUsername) {
        hasChanges = true;
    }
    
    // 检查住址是否修改
    var originalAddr = $('#addr').attr('data-original') || '';
    if (addr !== originalAddr) {
        hasChanges = true;
    }
    
    // 检查邮箱是否修改
    var originalEmail = $('#email').attr('data-original') || '';
    if (email !== originalEmail) {
        hasChanges = true;
    }
    
    // 检查密码是否填写
    if (password && password.trim() !== '') {
        hasChanges = true;
    }
    
    if (!hasChanges) {
        alert('请修改信息后再提交');
        return;
    }

    // 获取表单数据
    var formData = {
        original_username: originalUsername,
        username: username,
        addr: addr,
        password: password,
        email: email
    };

    // 显示加载状态
    var submitBtn = $(this).find('button[type="submit"]');
    var originalText = submitBtn.html();
    submitBtn.html('<i class="fa fa-spinner fa-spin"></i> 保存中...').prop('disabled', true);
    
    // 发送AJAX请求
    $.ajax({
        url: '/update_profile',
        type: 'POST',
        data: formData,
        dataType: 'json',
        success: function(response) {
            if (response.valid == '1') {
                alert('保存成功！');
                // 更新显示
                window.location.replace('/user/' + formData.username);
            } else {
                alert('保存失败：' + response.msg);
            }
        },
        error: function(xhr, status, error) {
            alert('请求失败，请重试');
            console.log('错误信息:', error);
        },
        complete: function() {
            // 恢复按钮状态
            submitBtn.html(originalText).prop('disabled', false);
        }
    });
});

// 密码显示/隐藏功能
$(document).ready(function() {
    $('#password-toggle').click(function(e) {
        e.preventDefault();
        var passwordInput = $('#password');
        var toggleIcon = $(this);
        
        if (passwordInput.attr('type') === 'password') {
            // 显示密码
            passwordInput.attr('type', 'text');
            toggleIcon.removeClass('fa-eye').addClass('fa-eye-slash');
            toggleIcon.addClass('show');
        } else {
            // 隐藏密码
            passwordInput.attr('type', 'password');
            toggleIcon.removeClass('fa-eye-slash').addClass('fa-eye');
            toggleIcon.removeClass('show');
        }
    });
});

// 重置按钮
$('#profile-form button[type="reset"]').click(function(e){
    e.preventDefault();

    // 重置表单
    $('#profile-form')[0].reset();
    
    // 延迟更新原始数据，确保表单重置完成
    setTimeout(function() {
        originalUsername = $('#username').val();
    }, 100);
});