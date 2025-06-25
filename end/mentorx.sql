/*
 Navicat Premium Dump SQL

 Source Server         : MentorX
 Source Server Type    : MySQL
 Source Server Version : 80031 (8.0.31)
 Source Host           : localhost:3306
 Source Schema         : mentorx

 Target Server Type    : MySQL
 Target Server Version : 80031 (8.0.31)
 File Encoding         : 65001

 Date: 24/06/2025 14:36:52
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for chapter
-- ----------------------------
DROP TABLE IF EXISTS `chapter`;
CREATE TABLE `chapter`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `content` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL,
  `course_id` int NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `refKey_course_id`(`course_id` ASC) USING BTREE,
  CONSTRAINT `refKey_course_id` FOREIGN KEY (`course_id`) REFERENCES `course` (`id`) ON DELETE CASCADE ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 35 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of chapter
-- ----------------------------
INSERT INTO `chapter` VALUES (6, 'TensorFlow.js应用开发', '### 七.1 认识TensorFlow.js  \r\n#### 知识讲解内容  \r\n\r\n**目标：**  \r\n了解 TensorFlow.js 的优点、相关概念以及其在浏览器环境中的应用。  \r\n\r\n**知识概述:**  \r\n- **简介与扩展版本**：TensorFlow.js 是 Google 开发的 JavaScript 版本，支持 GPU 加速，并可运行在 Node.js 或浏览器环境中。  \r\n- **应用场景**：可在网页端构建深度学习模型（如图片识别、语音处理等），并与其他 Python 模型互转。  \r\n- **功能优势**：  \r\n  - 支持 GPU 加速，提高运算效率。  \r\n  - 使用 JavaScript 开发，降低了编程门槛。  \r\n\r\n**核心概念与API:**  \r\n- **张量 (Tensor)**：中心数据单元是多维数组，定义其形状和值。使用 `tf.tensor` 创建张量并打印输出。  \r\n\r\n#### 实训练习安排  \r\n\r\n**第一项实践：利用DeepLearning.js 从头开发模型**  \r\n1. 使用 DeepLearning.js（基于 WebGL 加速）在浏览器上开发一个简单的图像识别模型（如图片分类）。  \r\n2. 基于预训练的 DeepLearn.js 模型，在网页端进行验证。  \r\n\r\n**第二项实践：TensorFlow.js 的高级功能与 Keras API**  \r\n1. 使用 TensorFlow.js 的 `Layers API` 或低级运算创建一个简单的神经网络模型。  \r\n2. 实现一个简单的神经网络，并在 Node.js 中测试其运行效果。  \r\n\r\n---\r\n\r\n### **指导建议（学生应掌握哪些技能/难点）**\r\n\r\n**目标：** 学生能够熟练使用 TensorFlow.js，包括理解其结构、使用 API 创建模型以及在不同环境中进行开发与部署。  \r\n\r\n**重点内容：**  \r\n1. **TensorFlow.js 的结构与功能**：了解它如何整合底层 Core API 和高级 Layers API，并掌握 GPU 加速的优势。  \r\n2. **环境配置与安装**：安装 TensorFlow.js 时，注意 Node.js 是否支持 CUDA 或 WebGL 链接，以及在浏览器中使用 JavaScript 的兼容性问题。  \r\n3. **张量操作与打印**：熟悉张量的创建、打印和形状查询功能。  \r\n4. **模型开发流程**：理解从数据预处理到模型构建、训练和部署的整体过程。  \r\n\r\n**难点与建议：**  \r\n- TensorFlow.js 中层 API 的高级特性可能对开发者来说是挑战，但可以通过逐步学习基础操作来克服。  \r\n- 在 Node.js 环境中运行模型时，确保其兼容性和性能优化需要特别注意。  \r\n\r\n---\r\n\r\n通过以上计划，学生将掌握TensorFlow.js 的基本概念、核心功能以及实际应用，从而能够熟练开发并部署深度学习模型', 3);
INSERT INTO `chapter` VALUES (8, 'Python程序设计', '### 课程名称：Python程序设计\n\n#### 知识讲解内容：\n1. **树莓派开发环境配置**  \n   - 打开终端窗口并执行 `python` 按钮以查看当前的 Python 版本（默认为 Python3.9.2）。  \n   - 如果需要升级，使用树莓派系统或第三方工具。  \n   - 设置路径和安装必要的依赖包。\n\n2. **变量类型与操作**  \n   - **字符串**：用于存储文本、信息等，如 `name = \"John\"`。  \n     - 运算符：`+`, `-`, `*`, `/`, `%`（整除和取余）。  \n     - 混合运算：括号控制优先级。  \n   - **整数**：用于表示数量、编号等，如 `$100`。  \n   - **浮点数**：表示具有小数部分的值，如 `3.5`。  \n\n3. **运算符与混合操作**  \n   - 加减乘除：按顺序执行优先级。  \n   - 取模（%）：计算余数。  \n   - 混合运算示例：`5 + 2 * 3 = 11`，因为先乘后加。\n\n4. **元组与列表**  \n   - **元组**：有序的访问，使用 `()` 表示。  \n   - **列表**：无序且可随机访问元素，使用 `[]` 表示。  \n\n#### 实训练习安排：\n1. **配置树莓派开发环境（2 课时）**  \n   - 使用 Python 打开终端，执行 `python` 查看版本和运行基本操作。  \n   - 确保路径正确，安装必要的依赖包如 pip3。\n\n2. **变量操作实验（2 课时）**  \n   - 创建变量并测试基本类型（字符串、整数、浮点数）。  \n   - 运算符练习：加减乘除和混合运算。  \n   - 元组与列表生成：`age = [\"18\", \"19\"]`，`scores = [75, 85]`。\n\n#### 指导建议：\n- **掌握技能**：了解 Python 基本语法、变量类型和操作规则。  \n- **难点理解**：区分运算符优先级（括号内优先），熟悉元组与列表的使用。  \n- **实践提升**：通过实际项目巩固变量应用，提高代码结构能力。\n\n#### 时间分布：\n1. 理论讲解（2 课时）  \n   - 树莓派开发环境配置、变量操作。  \n\n2. 实验实践（2 课时）  \n   - 配置环境、变量操作实验。  \n\n#### 指导建议总结：\n- 学生应熟悉字符串、整数和浮点数的类型，掌握基本运算符，并理解元组与列表的应用。', 4);
INSERT INTO `chapter` VALUES (9, '变量', '### 教学内容\n\n#### 知识讲解\n1. **树莓派Python开发环境的配置**\n   - 树莓派默认安装了**Python 3.x**开发环境（例如：Tree莓Pi Python v5.8）。\n   - 打开终端，执行以下命令检查当前版本：\n     ```bash\n     python --version\n     ```\n   - 如果树莓派没有安装**Python 3.x**或其他版本，可以进行升级：\n     - 使用**树莓派系统升级**工具（如：`treepirt-upsilon`）。\n     - 或者手动升级到目标版本（例如：升级到 Python 3.9）。\n   - 如果遇到升级错误或安装问题，可以通过以下方式排查：\n     - 检查是否缺少必要的依赖包（如 NumPy、Pandas 等）。\n     - 在终端中运行优化脚本，以适合特定的训练数据集。\n\n2. **变量与数据类型**\n   - Python 3.9 已经完全支持变量命名和赋值：\n     ```python\n     variable_name = value\n     ```\n   - 遵循**DRY (Don\'t Repeat Yourself)**原则（值只保留最后一次定义）。\n   - 掌握常见数据类型的使用：数字、字符串、布尔值等。\n\n3. **表达式与计算**\n   - 使用数学和逻辑运算符进行数值计算：\n     ```python\n     a = 5 + 3\n     b = 2 * 4\n     c = a + b\n     ```\n   - 理解并使用**字典、列表、集合**等数据结构进行更复杂的操作。\n\n4. **函数与方法**\n   - 在 Python 中定义函数：\n     ```python\n     def func():\n         print(\"Hello World!\")\n     ```\n   - 使用类和对象进行更复杂的操作。\n   - 掌握**类的命名和命名原则**（类、对象、 instance 等）。\n\n5. **文件与输入输出**\n   - 学会使用**input()**函数获取用户输入：\n     ```python\n     user_input = input(\"Enter your message: \")\n     print(user_input)\n     ```\n   - 学会使用**file**模块进行文件操作（例如读取/写入文件）。\n\n6. **调试和输出**\n   - 了解 Python 中的**try-except**语句用于处理异常。\n   - 掌握简单的**print()**函数和**input()**函数的基本用法。\n\n#### 实训练习安排\n\n1. **基础变量练习**\n   - 创建并打印多个变量：\n     ```python\n     a = 5\n     b = \'Hello\'\n     c = True\n     print(a, b, c)\n     ```\n   - 计算表达式并输出结果：\n     ```python\n     result = (2 + 3) * 4\n     print(result)\n     ```\n\n2. **使用字典和集合**\n   - 创建一个简单的字典并访问键值对：\n     ```python\n     my_dict = {\'name\': \'John\', \'age\': 30}\n     print(my_dict[\'name\'])\n     ```\n   - 使用列表进行简单的排序或遍历操作。\n\n3. **函数练习**\n   - 编写简单的函数并调用：\n     ```python\n     def greet():\n         print(\"Hello World!\")\n     \n     greet()\n     ```\n   - 掌握简单的**return**值功能。\n\n4. **输入输出与处理**\n   - 读取一行用户输入，并进行相应的输出：\n     ```python\n     user_input = input(\"Enter your message: \")\n     print(f\"{user_input}\")\n     ```\n   - 使用文件操作，将数据写入文件：\n\n#### 指导建议\n\n1. **掌握变量命名和赋值**\n   - 理解Python变量命名的原则（如 camelCase、snake_case等）。\n   - 学会通过实际项目选择合适的变量名。\n\n2. **了解基本的表达式和计算**\n   - 学习使用数学和逻辑运算符进行数值计算。\n   - 理解字符串操作中的特殊字符处理。\n\n3. **熟悉函数与方法**\n   - 学会定义简单功能性的函数。\n   - 掌握类的命名原则，并能设计简单的类结构。\n\n4. **学习文件与输入输出**\n   - 熟悉input()和print()函数的基本用法，能够根据需求选择合适的工具（如sys.stdin）进行输入。\n   - 学会使用file模块读取/写入数据。\n\n5. **调试与输出**\n   - 了解try-except语句在异常处理中的作用。\n   - 学会通过简单的print()函数验证变量和结果的正确性。\n\n#### 时间分布\n\n| 部分 | 节目 | 时间 |\n|-------|------|-----|\n| 知识讲解 | 第1节 9.1 | 40分钟 |\n| 实训练习 | 第2节 项目9.1 | 60分钟 |\n\n通过理论与实践结合的教学方式，可以帮助学生更好地掌握树莓派开发环境的配置以及Python的基础变量使用。同时，实践操作能让学生在实际应用中加深对知识点的理解，并提升解决问题的能力。', 4);
INSERT INTO `chapter` VALUES (34, '函数', '### 课程名称：Python程序设计\n\n#### **一、课程概述**\n本课程旨在帮助学生学习 Python 程序设计的基础知识，并将其应用于实际开发项目。通过配置树莓派的 Python 发开环境和进行量化转换，学生将掌握从基础编程概念到应用现代技术的技能。\n\n---\n\n### **二、课程结构**\n\n#### **第一部分：树莓派 Python 开发环境**\n1. **了解树莓派 Python 安装情况**  \n   - 树莓派默认安装了 Python 3.9.2，可以通过升级更改为其他版本。\n   \n2. **配置 Python 发开环境**  \n   - 绘制终端工具并运行 `python` 目前是否已安装了 Python 开发环境，并查看当前 Python 版本。  \n   - 高级用户可以使用以下方法升级树莓派系统：\n     ```python\n     treeerryapi Python 3.9.2 -> upgrade\n     ```\n\n3. **实际操作**  \n   - 示例代码：配置树莓派的开发环境并运行示例代码。\n   \n4. **输出分析**  \n   - 解释 interpreter.get_tensor() 和 class_names 的作用，并展示 score 计算过程。\n\n#### **第二部分：TensorFlow 量化转换**\n1. **TensorFlow 功能概述**  \n   - 探索 TensorFlow 如何将模型推理结果与现实世界联系起来，包括量化转换的步骤和实现方法。\n\n2. **代码示例解析**  \n   - 使用示例代码运行量化转换，并观察预测结果。\n   \n3. **理解代码逻辑**  \n   - 解释 interpreter.set_tensor 和 interpreter.invoke() 的作用，以及 score 计算过程中的数学运算。\n\n#### **第三部分：Android 解释器 初始化**\n1. **Android 解释器原理**  \n   - 学习如何使用 Android 解释器进行 Python 程序的解释与运行。\n\n2. **实际操作**  \n   - 示例代码示例：在 Android 设备上运行Python程序，并利用解释器获取预测结果。\n\n3. **输出解读**  \n   - 解析 interpreter.get_tensor() 的作用，理解类的概率计算过程。\n\n---\n\n### **三、教学建议**\n1. **掌握技能**  \n   - 了解树莓派作为开发者的重要平台。\n2. **解决难点**  \n   - 熟悉TensorFlow 在量化转换中的具体实现，优化参数以提高预测准确率。\n3. **拓展应用**  \n   - 将所学知识应用到实际项目中，提升编程能力和开发效率。\n\n---\n\n### **四、时间分布**\n- **第一部分：理论与实践（40%）**  \n  - 理论讲解与实践操作，包括配置环境和量化转换。\n- **第二部分：理论与实践（30%）**  \n  - 内容深入探讨TensorFlow 的功能及其实现逻辑。\n- **第三部分：理论与实践（20%）**  \n  - Android 解释器的使用实践。\n- **总结（15%）**  \n  - 总结本课程内容，强调实际应用的重要性。\n\n---\n\n### **五、预期成果**\n通过本课程，学生将掌握配置树莓派 Python 开发环境的基本技能，并能够进行量化转换和Android 解释器初始化。同时，将提升编程能力和解决现实世界的联系问题的逻辑思维能力。\n\n---\n\n### **六、指导建议**\n1. **学习资源**  \n   - 提供丰富的代码示例和实际项目，帮助学生实践。\n2. **在线工具**  \n   - 建议使用 Tree莓Py 的开发环境或其他 Python 环境进行实际练习。\n3. **问题解决**  \n   - 引导学生遇到的问题并提供指导，包括如何正确运行代码和优化量化转换参数。\n\n---\n\n### **七、总结**\n这门课程通过理论与实践相结合的方式，帮助学生掌握 Python 应用开发环境配置和量化转换能力。同时，学生将学习 Android 解释器的使用方法，并将这些技能应用到实际项目中，从而提升编程能力和解决现实世界的联系问题的能力。', 4);

-- ----------------------------
-- Table structure for communicate_history
-- ----------------------------
DROP TABLE IF EXISTS `communicate_history`;
CREATE TABLE `communicate_history`  (
  `student_id` int NULL DEFAULT NULL,
  `chapter_id` int NULL DEFAULT NULL,
  `type` char(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `content` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL,
  `time` datetime NULL DEFAULT NULL,
  `session_id` int NULL DEFAULT NULL,
  `session_name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  INDEX `refKey_student_id`(`student_id` ASC) USING BTREE,
  INDEX `refKey_chapter_id`(`chapter_id` ASC) USING BTREE,
  CONSTRAINT `refKey_chapter_id` FOREIGN KEY (`chapter_id`) REFERENCES `chapter` (`id`) ON DELETE CASCADE ON UPDATE RESTRICT,
  CONSTRAINT `refKey_student_id` FOREIGN KEY (`student_id`) REFERENCES `user` (`user_id`) ON DELETE CASCADE ON UPDATE RESTRICT
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of communicate_history
-- ----------------------------
INSERT INTO `communicate_history` VALUES (5, 6, 'Q', '我没有听懂TensorFlow.js的优点是什么，你能帮我吗？', '2025-06-23 17:17:39', 1, '默认名称');
INSERT INTO `communicate_history` VALUES (5, 6, 'A', 'TensorFlow.js 的优点主要体现在以下几个方面：\n\n1. **支持 GPU 加速**  \n   TensorFlow.js 是一个基于 JavaScript 的深度学习框架，结合了 Core API 和高级层 API（Layer API）。通过将运算直接映射到底层底层的 Core API，并将其扩展到高一层，可以更好地利用 GPU 加速计算。这意味着在某些任务中，即使不使用 GPU，也能达到与深度学习框架运行相同的性能甚至更好的效果。\n\n2. **支持多种环境**  \n   TensorFlow.js 可以在 Node.js 环境下运行，也可以在浏览器环境中直接构建模型（例如用于网页端的开发）。这对于开发者来说是一个很大的优势，因为它们可以在不同平台上轻松部署和运行模型。\n\n3. **降低编程门槛**  \n   与传统的深度学习框架（如 PyTorch）相比，TensorFlow.js 使用了 JS 的特性，使其更加易于理解和实现。此外，其 API 高级化（如通过 Layer API 实现复杂的网络结构），使得开发者可以在轻松的代码环境中构建和训练模型。\n\n4. **集成底层 Core API**  \n   TensorFlow.js 是 Core API 的扩展版本，它直接映射到底层的操作。这种高度绑定的特性确保了在处理复杂任务时，可以有效地利用 GPU 加速计算，并且可以无缝地与其他框架（如 NumPy）结合使用，进一步提升模型的性能。\n\n5. **扩展性和可扩展性**  \n   TensorFlow.js 是一个扩展型框架，可以根据需求添加新的功能和模块。此外，它还与 PyTorch 等其他深度学习框架实现了互操作性，使得开发者可以在多种平台上无缝切换工具链。\n\n### 实验内容：\n#### 第一项实践：利用DeepLearning.js 从头开发模型  \n- 使用 DeepLearning.js（基于 WebGL 加速）在浏览器上开发一个简单的图片识别模型（如图片分类）。  \n- 在网页端进行验证，并与其他 Python 模型互转。  \n\n#### 第二项实践：TensorFlow.js 的高级功能与 Keras API  \n- 使用 TensorFlow.js 的 `Layers API` 或低级运算创建一个神经网络模型。  \n- 实现一个简单的神经网络，并在 Node.js 中测试其运行效果。\n\n### 核心概念与API：\n1. **张量 (Tensor)**：中心数据单元是多维数组，定义其形状和值。使用 `tf.tensor` 创建张量并打印输出。  \n\n通过上述内容，你可以更全面地了解 TensorFlow.js 的优点及其在不同环境中的应用。', '2025-06-23 17:17:42', 1, '默认名称');
INSERT INTO `communicate_history` VALUES (7, 6, 'Q', '你好', '2025-06-24 09:15:26', 2, '默认名称');
INSERT INTO `communicate_history` VALUES (7, 6, 'A', '### 问题思考与答案\n\n**思考：**\n在深入理解TensorFlow.js及其在浏览器环境中的应用后，下面是一些可以用来提问并探索相关知识的综合问题：\n\n1. **张量的作用是什么？**  \n   张量在机器学习中是多维数组，其形状和值定义了数据单元。使用 `tf.tensor` 创建并打印输出可以帮助你熟悉这一概念。\n\n2. **DeepLearning.js 与 TensorFlow.js 的区别是什么？**  \n   DeepLearning.js 基于 WebGL加速，而 TensorFlow.js 使用 JavaScript 开发，适合较低水平的项目中。\n\n3. **TF Layers API 的高级特性有哪些？**  \n   可以通过使用低级运算构建复杂的神经网络模型，并在 Node.js 中测试其性能。\n\n4. **如何在浏览器环境中运行TensorFlow.js？**  \n   首先安装 Node.js，并确保它支持CUDA或WebGL链接，然后将 TensorFlow.js 加载到一个 HTML 文件中即可运行。\n\n5. **DeepLearning.js 在网页端的应用场景有哪些？**  \n   DeepLearning.js 可以用于快速构建图像识别模型，在网页端进行验证，适合快速开发和测试。\n\n6. **如何使用张量操作打印输出？**  \n   使用 `tf.tensor` 创建一个张量后，可以打印其形状、值并访问特定元素来理解其结构。\n\n7. **在Node.js环境下运行TensorFlow.js需要配置哪些部分？**  \n   需要安装相关的依赖包，并确保浏览器兼容性，通常包括正确导入模块和设置适当的环境变量。\n\n8. **如何从头开发一个简单的图像识别模型？**  \n   使用 DeepLearning.js 从头创建一个简单的图像分类任务，然后在网页端进行验证和测试，这能够帮助你熟悉整个过程。\n\n9. **神经网络的高级功能与 Keras API 的区别是什么？**  \n   在 TensorFlow.js 中使用 `Layers API` 或低级运算构建更复杂的模型，并与 Keras API 实现接口，适用于开发更复杂的问题。\n\n10. **TensorFlow.js 需要哪些配置参数才能高效运行？**  \n    通过配置 Node.js 和 CUDA/CUDA 模块，可以优化 TensorFlow.js 的性能，使其在浏览器中高效运行。', '2025-06-24 09:15:29', 2, '默认名称');
INSERT INTO `communicate_history` VALUES (7, 6, 'Q', '张量的作用是什么？', '2025-06-24 09:25:29', 2, '默认名称');
INSERT INTO `communicate_history` VALUES (7, 6, 'A', '**张量的作用是什么？**\n\n在 TensorFlow.js 中，张量是数据的基本单元，类似于多维数组，负责存储和表示数据。它们的关键作用在于：\n\n1. **数据存储与变换**：张量可以存储图像、文本或其他数据形式，并通过矩阵运算等方法进行变换。\n2. **高效计算**：TensorFlow.js 提供了高效的计算框架，能够在 GPU 上加速运算，显著提升速度。\n3. **深度学习模型处理**：支持对输入数据进行预处理和特征提取，促进模型训练的效率和效果。\n\n**步骤说明：**\n\n1. **创建张量**：\n   - 使用 `tf.tensor` 创建张量并打印输出。例如，创建一个形状为 (1, 2) 的二维张量。\n   \n2. **查询张量形状**：\n   - 计算张量的形状，了解数据结构和维度。\n   \n3. **进行矩阵运算**：\n   - 在张量上执行如矩阵乘法等操作，这是深度学习中的核心任务。\n\n通过这些步骤，理解了如何在 TensorFlow.js 中有效管理和操作数据张量，从而构建并训练深度学习模型。', '2025-06-24 09:25:32', 2, '默认名称');

-- ----------------------------
-- Table structure for course
-- ----------------------------
DROP TABLE IF EXISTS `course`;
CREATE TABLE `course`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `teacher` int NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `refKey_teacher_id`(`teacher` ASC) USING BTREE,
  CONSTRAINT `refKey_teacher_id` FOREIGN KEY (`teacher`) REFERENCES `user` (`user_id`) ON DELETE CASCADE ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 5 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of course
-- ----------------------------
INSERT INTO `course` VALUES (3, 'TensorFlow.js应用开发', 3);
INSERT INTO `course` VALUES (4, 'Python程序设计', 11);

-- ----------------------------
-- Table structure for course_student
-- ----------------------------
DROP TABLE IF EXISTS `course_student`;
CREATE TABLE `course_student`  (
  `course_id` int NOT NULL,
  `student_id` int NOT NULL,
  PRIMARY KEY (`course_id`, `student_id`) USING BTREE,
  INDEX `refKey_student_id_2`(`student_id` ASC) USING BTREE,
  CONSTRAINT `refKey_course_id_2` FOREIGN KEY (`course_id`) REFERENCES `course` (`id`) ON DELETE CASCADE ON UPDATE RESTRICT,
  CONSTRAINT `refKey_student_id_2` FOREIGN KEY (`student_id`) REFERENCES `user` (`user_id`) ON DELETE CASCADE ON UPDATE RESTRICT
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of course_student
-- ----------------------------
INSERT INTO `course_student` VALUES (3, 7);
INSERT INTO `course_student` VALUES (4, 7);
INSERT INTO `course_student` VALUES (3, 12);

-- ----------------------------
-- Table structure for exercise
-- ----------------------------
DROP TABLE IF EXISTS `exercise`;
CREATE TABLE `exercise`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `exercise_content` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL,
  `answer` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL,
  `difficulty` int NULL DEFAULT NULL,
  `type` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `chapter_id` int NULL DEFAULT NULL,
  `is_official` tinyint(1) NULL DEFAULT NULL COMMENT '1代表老师习题，0代表学生生成习题',
  `student_id` int NULL DEFAULT NULL COMMENT '生成习题的学生编号',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `refKey_chapter_id_3`(`chapter_id` ASC) USING BTREE,
  INDEX `refKey_student_id_3`(`student_id` ASC) USING BTREE,
  CONSTRAINT `refKey_chapter_id_3` FOREIGN KEY (`chapter_id`) REFERENCES `chapter` (`id`) ON DELETE CASCADE ON UPDATE RESTRICT,
  CONSTRAINT `refKey_student_id_3` FOREIGN KEY (`student_id`) REFERENCES `user` (`user_id`) ON DELETE CASCADE ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 14 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of exercise
-- ----------------------------
INSERT INTO `exercise` VALUES (8, '**练习题目：**\n\n在浏览器环境中使用 TensorFlow.js 创建并打印一个2x2的张量：\n\n1. 使用 `tf.tensor` 来创建一个2x2的二维数组表示数字矩阵：\n   ```javascript\n   const tensor = tf.tensor([[[[2, 2], [3, 3]], [[4, 4], [5, 5]]], [[[6, 6], [7, 7]], [[8, 8], [9, 9]]]])\n   ```\n2. 打印这个张量：\n   ```javascript\n   console.log(tensor)\n   ```\n\n**解答：**\n\n1. 使用 TensorFlow.js 创建一个二维数组：\n```javascript\nconst tensor = tf.tensor([[[[2, 2], [3, 3]], [[4, 4], [5, 5]]], [[[6, 6], [7, 7]], [[8, 8], [9, 9]]]])\n```\n2. 打印张量：\n```javascript\nconsole.log(tensor)\n```\n\n通过以上步骤，学生将实践 TensorFlow.js 创建和打印张量的能力。', '1. 使用 TensorFlow.js 创建一个简单的2x2的张量：\n```javascript\nconst tensor = tf.tensor([[2, 3], [4, 5]]);\n```\n\n2. 打印这个张量：\n```javascript\nconsole.log(tensor);\n```', 1, 'answers', 6, 1, NULL);
INSERT INTO `exercise` VALUES (10, '### 七.1 认识TensorFlow.js  \n\n**目标：**  \n通过本题，学生能够理解TensorFlow.js的基本概念、核心功能以及在浏览器环境中的应用。\n\n**题目内容：**  \n利用TensorFlow.js创建一个简单的张量和模型预测器。  \n\n1. 使用DeepLearning.js（基于 WebGL 加速）在浏览器上开发一个简单的图片分类模型（如图片分类）。  \n2. 基于预训练的 DeepLearn.js 模型，在网页端进行验证。  \n3. 通过将TensorFlow.js 张量和 API 应用到实际图像数据中，实现对一张图片的预测并输出结果。  \n\n**提示：**  \n- 使用 `tf.tensor` 创建张量，并打印出其形状和值。  \n- 在使用 DeepLearning.js 的基础模型时，确保其在 Node.js 中运行，同时确保 Node.js 支持 WebGL 加速。', '### **题目答案**\n\n**目标：**  \n通过本题，学生能够了解TensorFlow.js的基本概念、核心功能以及在浏览器环境中的实际应用。\n\n**题目内容：**  \n1. 使用DeepLearning.js（基于 WebGL 加速）在浏览器上开发一个简单的图片分类模型（如图片分类）。  \n2. 基于预训练的 DeepLearn.js 模型，在网页端进行验证。  \n3. 通过将TensorFlow.js 张量和 API 应用到实际图像数据中，实现对一张图片的预测并输出结果。\n\n**步骤说明：**\n\n1. **安装依赖**：确保 Node.js 支持 GPU 加速，并安装 DeepLearning.js 和 TensorFlow.js。\n\n2. **创建张量**：在浏览器中使用 `tf.tensor` 创建一个简单的张量实例。例如，创建一个形状为 (1, 2) 的整数张量并打印其形状和值：\n\n   ```javascript\n   const tensor = tf.tensor([1, 2]);\n   console.log(tensor.shape); // 输出: { shape: [2] }\n   console.log(tensor.value); // 输出: Array [[1], [2]]\n   \n   ```\n   这将生成一个形状为 `[1, 2]` 的整数张量。\n\n3. **构建模型**：使用 DeepLearn.js 基础模型（如图识别）进行开发。例如，使用以下结构搭建一个简单的图像分类模型：\n\n   ```javascript\n   const model = tf.Sequential({\n     // 输入层\n     tf.InputLayer,\n     // 中间层\n     tf.Dense(32, activation: \'relu\'),\n     // 输出层\n     tf.Dense(10, activation: \'softmax\')\n   });\n\n   model TensorFlow.compile();\n   \n   ```\n   这将生成一个包含前向传播和反向传播的图结构。\n\n4. **训练模型**：使用 DeepLearn.js 基础模型进行数据预处理（如归一化），然后开始训练。例如：\n\n   ```javascript\n   const train = model TensorFlowTrain({\n     // 预处理选项\n     tf.Normalize,\n     // 进行一定数量的迭代\n     epochs: 100,\n     // 训练验证循环的频率\n     validationFrequency: 25\n   });\n\n   ```\n   这将开始模型训练过程。\n\n5. **验证预训练模型**：在网页端使用预训练的 DeepLearn.js 模型进行验证。例如，输入一张图片数据后输出预测结果：\n\n   ```javascript\n   const input = tf.tensor([1, 2]); // 示例输入张量\n   const prediction = model(input); // 输出预测结果\n   console.log(prediction.shape); // 输出: { shape: [] }\n   console.log(prediction.value[0]); // 输出: 数字表示预测结果\n   ```\n\n6. **应用TensorFlow.js 张量**：将张量操作与 TensorFlow.js 的 API 应用到实际图像数据中进行预测。例如，使用以下步骤对一张图片进行处理：\n\n   - 读取图片数据（如 MNIST 数据集）。\n   - 使用 DeepLearning.js 基础模型中的某个层对图片数据进行前向传播。\n   - 将输出结果作为预测结果返回。\n\n通过以上步骤，学生能够理解TensorFlow.js 的基本概念、核心功能以及在浏览器环境中的实际应用。', 1, 'answers', 6, 0, 7);
INSERT INTO `exercise` VALUES (11, '**题目描述：**\n\n根据以下课件内容，请设计一道练习题目：\n\n### **知识概述:**\n\n- **张量 (Tensor)**：中心数据单元是多维数组，定义其形状和值。使用 `tf.tensor` 创建张量并打印输出。\n\n请在以下场景中创建一个 3x3 的张量，并输出该张量的形状：\n\n1. 当前网页上展示一张名为 \"Hello World\" 的图像。\n2. 在 Node.js 环境下运行并运行 TensorFlow.js 模型预测图片内容。', '1. 当前网页上展示一张名为 \"Hello World\" 的图像，并使用 `tf.tensor` 创建一个3x3的张量。打印该张量的形状。\n\n2. 在 Node.js 环境下运行并运行 TensorFlow.js 模型预测图片内容，使用 `tf.tensor([[[1, 2], [3, 4]], [[5, 6], [7, 8]]])` 创建一个3x3的张量。打印该张量的形状。\n\n答案：\n\n1. 当前网页上展示一张名为 \"Hello World\" 的图像，并使用 `tf.tensor` 创建一个3x3的张量。打印该张量的形状为：[[[1, 2], [3, 4]], [[5, 6], [7, 8]]]，形状是 2x2。\n\n2. 在 Node.js 环境下运行并运行 TensorFlow.js 模型预测图片内容，使用 `tf.tensor([[[1, 2], [3, 4]], [[5, 6], [7, 8]]])` 创建一个3x3的张量。打印该张量的形状为：[[[1, 2], [3, 4]], [[5, 6], [7, 8]]]，形状是 2x2。', 2, 'answers', 6, 0, 7);
INSERT INTO `exercise` VALUES (12, '### 选择题：\n\n1. **TensorFlow.js 是 Google 开发的 JavaScript 版本，支持 GPU 加速，并可运行在 Node.js 或浏览器环境中**。  \n   A. 正确  \n   B. 错误  \n\n2. 在Node.js中使用TensorFlow.js时可能遇到的问题是其不支持WebGL。  \n   A. 正确  \n   B. 错误  \n\n3. 张量的核心数据单元是多维数组，定义其形状和值。  \n   A. 正确  \n   B. 错误  \n\n4. 在 TensorFlow.js 中实现一个简单的神经网络模型需要逐步学习高级API。  \n   A. 正确  \n   B. 错误', '1. 正确  \n2. 正确  \n3. 正确  \n4. 正确', 1, 'choices', 6, 0, 7);
INSERT INTO `exercise` VALUES (13, '### 题目设计：\n\n#### 1. **树莓派 Python 发开环境配置与运行**\n**问题**：在树莓派环境中运行以下代码：\n```python\n# 运行示例代码（树莓派开发环境配置）\nimport treeerryapi\n\ntreeerryapi Python 3.9.2 -> upgrade\n\ndef hello():\n    print(\"Hello, Treeberry!\")\nprint(hello())\n```\n**输出分析**：解释 interpreter.get_tensor() 和 class_names 的作用，并展示 score 计算过程。\n\n---\n\n#### 2. **TensorFlow 量化转换实现**\n**问题**：使用示例代码运行TensorFlow的量化转换功能：\n```python\n# 在树莓派中进行量化转换\nimport tensorflow as tf\n\n# 创建模型\nmodel = tf.keras.applications.DenseNet121()\n\n# 假设模型预测结果为0.75，预测概率为90%\nscore = model.predict([[0.75]])\nscore = score[0][0]\n```\n**输出分析**：解释 interpreter.set_tensor 和 interpreter.invoke() 的作用，并展示 score 计算过程中的数学运算。\n\n---\n\n#### 3. **Android 解释器运行与结果解读**\n**问题**：在Android设备上运行以下Python代码并获取预测结果：\n```python\n# 在 Android 设备上运行 Python 程序\nimport treeerryapi\n\n# 示例代码\ndef main():\n    print(\"Android Device: Samsung S9\")\n    interpreter.get_tensor()\n    interpreter.invoke(\"predict\", [0.75])\n\nif __name__ == \"__main__\":\n    main()\n```\n**输出解读**：解析 interpreter.get_tensor() 的作用，理解类的概率计算过程。\n\n---\n\n### 课程目标与预期成果：\n\n1. 学会使用 Tree莓Py 的 Python 发开环境配置技能。\n2. 掌握TensorFlow 在量化转换中的实际应用，提升预测结果的准确性。\n3. 熟练Android 解释器的基础使用方法，并理解运行结果的含义。\n\n通过以上练习题，学生能够全面掌握树莓派 Python、TensorFlow 和 Android 解释器的核心功能，并将这些技能应用于实际项目中。', '### 1. 树莓派 Python 发开环境配置与运行分析\n\n**问题描述：**\n运行示例代码：\n```python\n# 运行示例代码（树莓派开发环境配置）\nimport treeerryapi\n\ntreeerryapi Python 3.9.2 -> upgrade\n\ndef hello():\n    print(\"Hello, Treeberry!\")\nprint(hello())\n```\n\n**输出分析：**\n\n- **解释 interpreter.get_tensor() 的作用：**\n  - `interpreter.get_tensor()` 提供了一种方式来获取模型张量数据。在机器学习模型训练和预测过程中，张量通常是输入特征或输出结果的一部分。通过解析这些张量的数据，可以提取重要的特征信息或直接使用模型的输出结果。\n\n- **解释 class_names 的作用：**\n  - `class_names` 是一个预定义的列表，通常用于存储模型或某种分类对象的类别名。在量化转换中，类名可能用来标识不同的预测结果或类别标签，便于后续分析和展示。\n\n**计算过程展示：**\n\n```python\nimport treeerryapi\n\ntreeerryapi Python 3.9.2 -> upgrade\n\ndef hello():\n    print(\"Hello, Treeberry!\")\nprint(hello())\n\n# 调试示例代码\nhello()\n```\n\n在运行时，`model.predict([[0.75]])` 的计算过程是：\n1. 将预测结果 `0.75` 转换为概率。\n2. 使用 sigmoid 函数（或类似激活函数）将输出转换为概率值。\n\n**结论：**\n通过 interpreter.get_tensor 和 class_names，代码能够提取模型特征并分类标签，展示出量化转换后的预测结果和对应的类别名。\n\n---\n\n### 2. TensorFlow 量化转换实现分析\n\n**问题描述：**\n使用示例代码运行TensorFlow的量化转换功能：\n```python\n# 在树莓派中进行量化转换\nimport tensorflow as tf\n\n# 创建模型\nmodel = tf.keras.applications.DenseNet121()\n\n# 假设模型预测结果为0.75，预测概率为90%\nscore = model.predict([[0.75]])\nscore = score[0][0]\n```\n\n**输出分析：**\n\n- **解释 interpreter.set_tensor 和 interpreter.invoke()的作用：**\n  - `interpreter.set_tensor` 将特定的数据代入到张量中。在量化转换中，通常是将模型的输入样本输入到预训练模型的网络结构中。\n  - `interpreter.invoke()` 调用被执行的指令或函数，并返回结果。在这里，`model.predict([[0.75]])` 是调用了一个名为 `predict` 的函数，用于模型预测。\n\n- **解释 score 计算过程中的数学运算：**\n  ```python\n  score = model.predict([[0.75]])\n  score = score[0][0]\n  ```\n\n**计算步骤：**\n\n1. 输入样本 `[[0.75]]` 被预训练模型 `DenseNet121` 执行。\n2. 模型输出为 `[0.9]`（概率表示）。\n3. 提取第一个样本的预测结果并转为概率。\n\n**结论：**\n通过 interpreter.set_tensor 和 invoke()，代码能够将输入样本代入模型，并正确进行量化转换，最终得到量化后预测的结果和概率值。\n\n---\n\n### 3. Android 解释器运行与结果解读分析\n\n**问题描述：**\n在Android设备上运行以下Python代码并获取预测结果：\n```python\n# 在 Android 设备上运行 Python 程序\nimport treeerryapi\n\n# 示例代码\ndef main():\n    print(\"Android Device: Samsung S9\")\n    interpreter.get_tensor()\n    interpreter.invoke(\"predict\", [0.75])\n\nif __name__ == \"__main__\":\n    main()\n```\n\n**输出解读：**\n\n- **解析 interpreter.get_tensor() 的作用：**\n  - `interpreter.get_tensor()` 提供了一种方式来访问模型张量的数据。在Android设备上运行的代码需要将预训练模型的特征提取结果获取到代码中，以便进行预测。\n\n- **理解类的概率计算过程：**\n  - 预处理输入样本 `0.75` 到 DenseNet121 模型中。\n  - 模型输出为 `[0.9]` 的概率，表示该图像属于某个特定类别。\n\n**结论：**\n通过 interpreter.get_tensor() 获取模型张量数据后，`interpreter.invoke(\"predict\", [0.75])` 运行了模型预测。结果 `[0.9]` 表示预测的概率为 90%，并通过 `class_names` 显示类名并展示概率计算过程。\n\n---\n\n### 总结：\n\n1. **树莓派 Python 的使用：**\n   - 配置环境、运行示例代码，理解 interpreter.get_tensor() 和 class_names。\n   \n2. **TensorFlow 量化转换：**\n   - 创建模型、进行量化转换，理解 interpreter.set_tensor 和 invoke()的作用。\n\n3. **Android 解释器的应用：**\n   - 在 Android 设备上运行代码，解析结果并理解示例中的概率计算过程。', 1, 'blanks', 34, 1, NULL);

-- ----------------------------
-- Table structure for practice_history
-- ----------------------------
DROP TABLE IF EXISTS `practice_history`;
CREATE TABLE `practice_history`  (
  `student_id` int NULL DEFAULT NULL,
  `exercise_id` int NULL DEFAULT NULL,
  `student_answer` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL,
  `analyse` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL,
  `check` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL,
  `time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `chapter_id` int NULL DEFAULT NULL,
  INDEX `refKey_student_id_4`(`student_id` ASC) USING BTREE,
  INDEX `refKey_chapter_id_4`(`chapter_id` ASC) USING BTREE,
  INDEX `refKey_exercise_id_4`(`exercise_id` ASC) USING BTREE,
  CONSTRAINT `refKey_chapter_id_4` FOREIGN KEY (`chapter_id`) REFERENCES `chapter` (`id`) ON DELETE CASCADE ON UPDATE RESTRICT,
  CONSTRAINT `refKey_exercise_id_4` FOREIGN KEY (`exercise_id`) REFERENCES `exercise` (`id`) ON DELETE CASCADE ON UPDATE RESTRICT,
  CONSTRAINT `refKey_student_id_4` FOREIGN KEY (`student_id`) REFERENCES `user` (`user_id`) ON DELETE CASCADE ON UPDATE RESTRICT
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of practice_history
-- ----------------------------
INSERT INTO `practice_history` VALUES (5, 8, 'printf(\"Hello, world!\");', '关键点：\n- 学生正确创建了一个2x2的二维数组，并将其转换为张量。\n- 张量被正确打印出来。\n- 使用了TensorFlow.js库。\n\n错误点：\n- 未考虑嵌套层数的问题，可能会影响性能和可维护性。\n- 打印张量时没有换行符，可能导致内容不完整或格式混乱。\n\n改进点：\n1. 简化结构：使用更合理的二维数组嵌套方式。\n2. 调整打印方式：确保换行符正确，提高输出清晰度。\n3. 确保环境和库正确配置，避免性能问题。', '批改结果：\n1. 正确性：否\n2. 部分正确：否\n3. 答案是否正确：否\n\n总评分：0分', '2025-06-23 15:39:37', 6);
INSERT INTO `practice_history` VALUES (7, 8, '111', NULL, NULL, '2025-06-23 17:52:55', 6);
INSERT INTO `practice_history` VALUES (7, 10, '1111', '**分析学生答案：**\n\n学生的回答是“1111”，表示他们完成了某些简单的代码块或问题，但没有按照实验步骤完成完整的任务。\n\n### 关键点：\n1. **使用张量操作**：如`tf.tensor([1, 2])`创建张量，并打印其形状和值。\n   - 正确性：正确使用了TensorFlow.js的tensors功能，展示了理解张量的操作。\n   \n2. **构建模型**：使用DeepLearning.js或TensorFlow.js搭建基本图像分类模型。\n   - 正确性：展示了对模型架构的理解，包括输入层、中间层和输出层。\n   \n3. **训练与验证**：利用预训练模型进行验证并进行预测。\n   - 正确性：确认了使用模型进行预测的步骤，显示了模型的实际应用能力。\n\n### 错误点：\n1. **代码不完整或错误**：生成的代码未完成实验流程。\n   - 学生可能只完成了部分任务或写错了代码，导致答案不完整。\n   \n2. **输出格式错误**：仅输出了简单的数字而不是展示模型预测结果。\n   - 学生可能在示例中没有正确解释结果，或者直接输出了数字而非进行模型验证和应用。\n\n### 改进之处：\n1. **详细实施实验流程**：要求学生完整地执行每个步骤，并正确使用TensorFlow.js的API。\n   - 提高学生对TensorFlow.js的理解和能力，确保他们能够完成完整的项目任务。\n\n2. **展示代码片段和解释**：提供清晰的示例代码，并在代码中包含详细的解释。\n   - 帮助学生更清楚地看到如何实现每个步骤，并理解每一步的作用。\n\n3. **输出模型预测结果**：确认模型的验证步骤，并展示预期的预测结果，以验证学生的实际应用能力。\n   - 通过展示实际应用的结果，帮助学生验证他们是否能够正确使用TensorFlow.js进行图像分类。\n\n4. **说明张量操作**：明确解释如何使用tensors进行数据处理和计算。\n   - 帮助学生更好地理解如何将张量操作应用于实际的图像数据中进行预测。', '根据用户提供的练习题答案和步骤说明，其中最后一部分输出只显示了一个数值且未呈现预测结果，这说明该部分未能完整执行。因此，步骤6中的预测结果没有正确展示。\n\n**批改结果：**\n- 步骤1、2、3、4、5均正确。\n- 步骤6未完成，只输出了数字1111，显示为错误（1）。\n\n请检查并完善该部分以实现完整的图片分类预测。', '2025-06-23 18:25:05', 6);
INSERT INTO `practice_history` VALUES (7, 12, 'A A A A', '### 分析：\n\n1. **TensorFlow.js 是否支持 GPU 加速？**  \n   - 学生选正确（正确），参考答案也是正确。\n\n2. **在Node.js中使用TensorFlow.js时可能遇到的问题是什么？**  \n   - 学生选正确（正确），参考答案也是正确，说明问题主要涉及其他方面如不支持WebGL，但此处学生没有错误选项。\n\n3. **张量的核心数据单元是多维数组吗？**  \n   - 学生选正确（正确），参考答案也是正确，这表明该描述无误。\n\n4. **实现简单神经网络模型是否需要学习高级API？**  \n   - 学生选正确（正确），参考答案也是一致的。\n\n### 总结：\n\n学生的作答在所有题目中均为正确，主要集中在第3题可能涉及其他因素如WebGL支持等方面。如果有特殊情况需确认，否则结论为正确。', '本批改结果如下：\n\n1. ** TensorFlow.js 是 Google 开发的 JavaScript 版本，支持 GPU 加速，并可运行在 Node.js 或浏览器环境中**。  \n   - 评分：0（正确）\n\n2. 在Node.js中使用TensorFlow.js时可能遇到的问题是其不支持WebGL。  \n   - 评分：0（正确）\n\n3. 张量的核心数据单元是多维数组，定义其形状和值。  \n   - 评分：0（正确）\n\n4. 在 TensorFlow.js 中实现一个简单的神经网络模型需要逐步学习高级API。  \n   - 评分：0（正确）', '2025-06-24 09:49:29', 6);

-- ----------------------------
-- Table structure for system_stats
-- ----------------------------
DROP TABLE IF EXISTS `system_stats`;
CREATE TABLE `system_stats`  (
  `AIchat` int NULL DEFAULT NULL,
  `generate_exercises` int NULL DEFAULT NULL,
  `check_exercises` int NULL DEFAULT NULL,
  `generate_teachcontent` int NULL DEFAULT NULL,
  `generate_tasks` int NULL DEFAULT NULL,
  `check` int NULL DEFAULT NULL
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of system_stats
-- ----------------------------
INSERT INTO `system_stats` VALUES (1, 2, 3, 4, 5, 6);

-- ----------------------------
-- Table structure for user
-- ----------------------------
DROP TABLE IF EXISTS `user`;
CREATE TABLE `user`  (
  `user_id` int NOT NULL AUTO_INCREMENT,
  `phone_number` varchar(12) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `password` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `type` char(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '用户类别',
  `frequence` int NOT NULL DEFAULT 0 COMMENT '使用频数',
  `sum_time` int NOT NULL DEFAULT 0 COMMENT '使用累计时间',
  `name` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `gender` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  PRIMARY KEY (`user_id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 13 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of user
-- ----------------------------
INSERT INTO `user` VALUES (3, '12345678910', '123456', 'T', 0, 0, '图图妈', 'female');
INSERT INTO `user` VALUES (4, '12345678911', '123456', 'A', 0, 0, '牛爷爷', 'male');
INSERT INTO `user` VALUES (5, '18736599391', '123456', 'S', 0, 0, '胡图图', 'male');
INSERT INTO `user` VALUES (6, '13967360428', '990923', 'T', 1, 4, '宋彧', 'male');
INSERT INTO `user` VALUES (7, '4095', '123456', 'S', 0, 0, 'wjy', 'unknow');
INSERT INTO `user` VALUES (10, '110', '123', 'A', 3, 161148, '管理', 'male');
INSERT INTO `user` VALUES (11, '4096', '123456', 'T', 0, 0, 'wjy', 'male');
INSERT INTO `user` VALUES (12, '111', '111', 'S', 0, 5929, '111', 'male');

SET FOREIGN_KEY_CHECKS = 1;
