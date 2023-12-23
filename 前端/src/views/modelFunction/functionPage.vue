<script setup>
import { ref } from 'vue'
import { Aim, Plus } from '@element-plus/icons-vue'
import PageContainer from '@/components/PageContainer.vue'
import { uploadImg } from '@/api/user'

const imgUrl = ref('')
const imgReceived = ref('')
const uploadRef = ref()
const onSelectFile = (uploadFile) => {
  // 基于 FileReader 读取图片做预览
  const reader = new FileReader()
  reader.readAsDataURL(uploadFile.raw)
  reader.onload = () => {
    imgUrl.value = reader.result
  }
}
const text = ref({
  prompt: '',
  step: ''
})

const textUpload = async () => {
  const res = await fetch('http://127.0.0.1:5000/t2i', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ text: text.value.prompt, step: text.value.step })
  })
  const responseData = await res.json()
  const base64Image = responseData.image
  const imgReceived = document.getElementById('imgReceived')
  imgReceived.src = `data:image/png;base64,${base64Image}` // 调整 MIME 类型以匹配实际的图片格式
  imgReceived.height = 300
  imgReceived.width = 300
}
const ImgUpload = async () => {
  const res = await fetch('http://127.0.0.1:5000/i2i', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ text: imgUrl.value })
  })
  const responseData = await res.json()
  const base64Image = responseData.images
  const imgReceived = document.getElementById('imgReceived')
  imgReceived.src = `data:image/png;base64,${base64Image}`; // 调整 MIME 类型以匹配实际的图片格式
  imgReceived.height = 300
  imgReceived.width = 300
}
</script>

<template>
  <page-container title="核心功能" class="beijing">
    <el-upload
      ref="uploadRef"
      :auto-upload="false"
      class="avatar-uploader"
      :show-file-list="false"
      :on-change="onSelectFile"
    >
      <img v-if="imgUrl" :src="imgUrl" class="avatar" />
      <el-icon v-else class="avatar-uploader-icon">
        <Plus />
      </el-icon>
    </el-upload>

    <br />

    <el-button
      @click="uploadRef.$el.querySelector('input').click()"
      type="primary"
      :icon="Plus"
      size="large"
      >选择图片
    </el-button>
    <el-button @click="ImgUpload" type="success" :icon="Aim" size="large"
      >图片修复
    </el-button>
    <br /><br />
    <el-input size="small" v-model="text.prompt" placeholder="提示词" />
    <br /><br />
    <el-input size="small" v-model="text.step" placeholder="step" />
    <br /><br />
    <el-button @click="textUpload" type="success" :icon="Aim" size="large"
      >图片生成
    </el-button>
    <br /><br /><br /><br />
    <img id="imgReceived" height="278" width="278" />
    <!-- 这是要修改的 img 元素 -->
  </page-container>
</template>

<style lang="scss" scoped>
.beijing {
  background: url('../../assets/wallhaven-yxkzdx_1280x1024.png') no-repeat
    center;
}

.avatar-uploader {
  :deep() {
    .avatar {
      width: 278px;
      height: 278px;
      display: block;
    }

    .el-upload {
      border: 1px dashed var(--el-border-color);
      border-radius: 6px;
      cursor: pointer;
      position: relative;
      overflow: hidden;
      transition: var(--el-transition-duration-fast);
    }

    .el-upload:hover {
      border-color: var(--el-color-primary);
    }

    .el-icon.avatar-uploader-icon {
      font-size: 28px;
      color: #8c939d;
      width: 278px;
      height: 278px;
      text-align: center;
    }
  }
}
</style>
