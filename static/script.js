$(document).ready(function() {
  // 功能1：隐藏
  $('#hideButton').click(function() {
    // 获取上传的两个二维码图片文件
    var qrCode1 = $('#qrCode1')[0].files[0];
    var qrCode2 = $('#qrCode2')[0].files[0];

    // 创建FormData对象，用于发送文件数据到后端
    var formData = new FormData();
    formData.append('qrCode1', qrCode1);
    formData.append('qrCode2', qrCode2);

    // 发送POST请求到后端处理隐藏操作
    $.ajax({
      url: '/hide', // 后端处理隐藏操作的URL
      type: 'POST',
      data: formData,
      processData: false,
      contentType: false,
      success: function(response) {
        var img = new Image();
        img.onload = function() {
          // 图像加载完成后设置src属性
          $('#imageContainer1').empty().append(img);
          $(img).css('z-index', '9999');
        };
        img.src = 'data:image/png;base64,' + response.imageData;
      }
    });
  });

  // 功能2：分割
  $('#splitButton').click(function() {
    // 获取上传的图片文件
    var inputImage = $('#inputImage')[0].files[0];
    // 获取输入框的二维码版本号
    var qrVersion = $('#qrVersion').val();
    // 创建FormData对象，用于发送文件数据到后端
    var formData = new FormData();
    formData.append('inputImage', inputImage);
    formData.append('qrVersion', qrVersion);

    // 发送POST请求到后端处理分割操作
    $.ajax({
      url: '/extract', // 后端处理分割操作的URL
      type: 'POST',
      data: formData,
      processData: false,
      contentType: false,
      success: function(response) {
        var img = new Image();
        img.onload = function() {
          // 图像加载完成后设置src属性
          $('#imageContainer2').empty().append(img);
        };
        img.src = 'data:image/png;base64,' + response.imageData;
      }
    });
  });
});
