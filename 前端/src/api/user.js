import request from '@/utils/request'

// 注册接口
export const userRegisterService = ({ userName, password, rePassword }) =>
  request.post('/user/register', { userName, password, rePassword })

// 登录接口
export const userLoginService = ({ userName, password }) =>
  request.post('/user/login', { userName, password })
//文生图
export const txtToImg = ({ prompt, step }) =>
  request.post('/img/text', { prompt, step })
// 获取用户基本信息
export const userGetInfoService = () => request.get('/user/getInfo')

// 更新用户基本信息
export const userUpdateInfoService = ({ id, nickname, email }) =>
  request.put('/user/updateUserInfo', { id, nickname, email })

//上传图片
export const uploadImg = (img) =>
    request.post('/img/upload',{img})

// 更新用户头像
export const userUpdateAvatarService = (avatar) =>
  request.patch('/user/updateAvatar', { avatar })

// 更新用户密码
export const userUpdatePasswordService = ({ oldPwd, newPwd, rePwd }) =>
  request.patch('/user/updatePwd', { oldPwd, newPwd, rePwd })
