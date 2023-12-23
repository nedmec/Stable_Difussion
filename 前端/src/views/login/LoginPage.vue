<script setup>
import { userRegisterService, userLoginService } from '@/api/user.js'
import { User, Lock } from '@element-plus/icons-vue'
import { ref, watch } from 'vue'
import { useUserStore } from '@/stores'
import { useRouter } from 'vue-router'
import Vcode from 'vue3-puzzle-vcode'

const isShow = ref(false)

const onClose = () => {
  isShow.value = false
}

const onSuccess = () => {
  onClose() // 验证成功，手动关闭模态框
}

const isRegister = ref(false)
const form = ref()

// 整个的用于提交的form数据对象
const formModel = ref({
  userName: '',
  password: '',
  rePassword: ''
})
// 整个表单的校验规则

const rules = {
  userName: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 2, max: 10, message: '用户名必须是 5-10位 的字符', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    {
      pattern: /^\S{6,15}$/,
      message: '密码必须是 6-15位 的非空字符',
      trigger: 'blur'
    }
  ],
  rePassword: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    {
      pattern: /^\S{6,15}$/,
      message: '密码必须是 6-15位 的非空字符',
      trigger: 'blur'
    },
    {
      validator: (rule, value, callback) => {
        // 判断 value 和 当前 form 中收集的 password 是否一致
        if (value !== formModel.value.password) {
          callback(new Error('两次输入密码不一致'))
        } else {
          callback() // 就算校验成功，也需要callback
        }
      },
      trigger: 'blur'
    }
  ]
}

const register = async () => {
  // 注册成功之前，先进行校验，校验成功 → 请求，校验失败 → 自动提示
  await form.value.validate()
  await userRegisterService(formModel.value)
  ElMessage.success('注册成功')
  isRegister.value = false
}

const userStore = useUserStore()
const router = useRouter()
const login = async () => {
  isShow.value = true
  await form.value.validate()
  const res = await userLoginService(formModel.value)
  userStore.setToken(res.data.token)
  ElMessage.success('登录成功')
  router.push('/')
}

// 切换的时候，重置表单内容
watch(isRegister, () => {
  formModel.value = {
    userName: '',
    password: '',
    rePassword: ''
  }
})
</script>

<template>

  <el-row class="login-page">
    <!--    <el-col :span="12" class="bg"></el-col>-->
    <el-col :span="10" :offset="8" class="form">
      <!-- 注册相关表单 -->
      <el-form
          :model="formModel"
          :rules="rules"
          ref="form"
          size="large"
          autocomplete="off"
          v-if="isRegister"
      >
        <el-form-item class="segment">
          <h1>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Sign Up</h1>
        </el-form-item>
        <el-form-item  prop="username">
          <el-input
              class="input"
              v-model="formModel.userName"
              :prefix-icon="User"
              placeholder="请输入用户名"
              clearable
          ></el-input>
        </el-form-item>
        <el-form-item  prop="password">
          <el-input
              class="input"
              v-model="formModel.password"
              :prefix-icon="Lock"
              type="password"
              placeholder="请输入密码"
              show-password
              clearable
          ></el-input>
        </el-form-item>
        <el-form-item prop="repassword">
          <el-input
              class="input"
              v-model="formModel.rePassword"
              :prefix-icon="Lock"
              type="password"
              placeholder="请输入再次密码"
              show-password
              clearable
          ></el-input>
        </el-form-item>
        <el-form-item>
          <el-button
              @click="register"
              class="button"
              type="primary"
              auto-insert-space
          >
            注册
          </el-button>
        </el-form-item>
        <el-form-item class="flex">
          <el-link type="info" :underline="false" @click="isRegister = false">
            ← 返回
          </el-link>
        </el-form-item>
      </el-form>

      <!-- 登录相关表单 -->
      <el-form
          :model="formModel"
          :rules="rules"
          ref="form"
          size="large"
          autocomplete="off"
          v-else
      >
        <el-form-item class="segment">
          <h1>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Log In</h1>
        </el-form-item>
        <el-form-item prop="username">
          <el-input
              class="input"
              v-model="formModel.userName"
              :prefix-icon="User"
              placeholder="请输入用户名"
              clearable
          ></el-input>
        </el-form-item>
        <el-form-item prop="password">
          <el-input
              class="input"
              v-model="formModel.password"
              name="password"
              :prefix-icon="Lock"
              type="password"
              placeholder="请输入密码"
              show-password
              clearable
          ></el-input>
        </el-form-item>

        <el-form-item>
          <Vcode :show="isShow" @success="onSuccess" @close="onClose" />
          <el-button
              @click="login"
              class="button"
              type="primary"
            auto-insert-space
            >登录</el-button
          >
        </el-form-item>
        <el-form-item class="flex">
          <el-link type="info" :underline="false" @click="isRegister = true">
            注册 →
          </el-link>
        </el-form-item>
      </el-form>
    </el-col>
  </el-row>
</template>

<style lang="scss" scoped>
.login-page {
  background: url('../../assets/wallhaven-1p398w_1880x940.png') no-repeat center
  center fixed;
  background-size: 100% 100%;
  width: 100%;
  height: 100vh;

  position: fixed;
  z-index: 1;
  margin: 0;

  .form {
    display: flex;
    flex-direction: column;
    justify-content: center;
    user-select: none;
    padding: 16px;
    width: 40%;
    margin: 0 auto;
    .segment {
      padding: 32px 0;
      display: flex;
      text-align: center;
    }
    h1 {
      margin: 0;
      font-size: 2.5vw;
      color: #babecc;
      text-shadow: 1px 1px 1px #fff;
    }
    .title {
      margin: 0 auto;
    }
    .input {
      font-family: 'Montserrat', sans-serif;
      letter-spacing: -0.2px;
      font-size: 20px;

      border: 0;
      outline: 0;
      border-radius: 320px;
      padding: 16px;
      background-color: #ebecf0;
      text-shadow: 1px 1px 0 #fff;
      display: flex;
      justify-content: center;
      align-items: center;

      margin-right: 8px;
      box-shadow: inset 2px 2px 5px #babecc, inset -5px -5px 10px #fff;
      width: 100%;
      box-sizing: border-box;
      transition: all 0.2s ease-in-out;
      appearance: none;
      -webkit-appearance: none;
    }
    .button {
      width: 100%;
      height: 60px;
      font-family: 'Montserrat', sans-serif;
      letter-spacing: -0.1px;
      font-size: 22px;
      display: block;

      border: 0;
      outline: 0;
      border-radius: 320px;
      padding: 16px;
      background-color: #ebecf0;
      text-shadow: 1px 1px 0 #fff;

      justify-content: center;
      align-items: center;

      color: #61677c;
      font-weight: bold;
      box-shadow: -5px -5px 20px #fff, 5px 5px 20px #babecc;
      transition: all 0.2s ease-in-out;
      cursor: pointer;
    }
    button:hover {
      box-shadow: -2px -2px 5px #fff, 2px 2px 5px #babecc;
    }
    button:active {
      box-shadow: inset 1px 1px 2px #babecc, inset -1px -1px 2px #fff;
    }
    button .icon {
      margin-right: 8px;
    }
    button.unit {
      border-radius: 8px;
      line-height: 0;
      width: 4vw;
      height: 4vw;
      display: inline-flex;
      justify-content: center;
      align-items: center;
      margin-right: 3vw;
      font-size: 19px;
    }
    button.unit .icon {
      margin-right: 0;
    }
    button.red {
      display: block;
      width: 100%;
      color: #ae1100;
    }
    .flex {
      width: 100%;
      display: flex;
      justify-content: space-between;
    }
  }
}
</style>
