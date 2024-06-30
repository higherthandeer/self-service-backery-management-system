// 常量路由：任意用户都可以访问到的路由
export const constantRoute = [
  // 路由模式
  // 登录
  {
    // 登陆页面
    path: '/login',
    component: () => import('@/views/login/index.vue'),
    name: 'login',
    meta: {
      title: '登录', // 菜单标题
      hidden: true, // 代表是否隐藏
      icon: 'Promotion', // 图标
    },
  },
  // 注册
  {
    path: '/register',
    component: () => import('@/views/register/index.vue'),
    name: 'register',
    meta: {
      title: '注册', // 菜单标题
      hidden: true, // 代表是否隐藏
      // icon: 'Promotion', // 图标
    },
  },
  // 主页
  {
    // 登陆成功后主页
    path: '/',
    component: () => import('@/layout/index.vue'),
    name: 'layout',
    meta: {
      title: '', // 菜单标题
      hidden: false, // 代表是否隐藏
      // icon: '',
    },
    redirect: '/home',
    children: [
      {
        path: '/home',
        component: () => import('@/views/home/index.vue'),
        meta: {
          title: '首页', // 菜单标题
          hidden: false, // 代表是否隐藏
          icon: 'House',
        },
      },
    ],
  },
  // 个人中心
  {
    path: '/user/center',
    component: () => import('@/layout/index.vue'),
    name: 'userCenter',
    meta: {
      title: '', // 菜单标题
      hidden: true, // 代表是否隐藏
      // icon: 'Box',
    },
    redirect: '/user/center',
    children: [
      {
        path: '/user/center',
        component: () => import('@/views/userCenter/index.vue'),
        name: 'userCenter',
        meta: {
          title: '个人中心', // 菜单标题
          hidden: true, // 代表是否隐藏
          // icon: 'Promotion', // 图标
        },
      },
    ],
  },

  // 修改密码页面
  {
    path: '/update/pwd',
    name: 'updatePwd',
    component: () => import('@/views/updatePwd/index.vue'),
    meta: {
      title: '修改密码', // 菜单标题
      hidden: true, // 代表是否隐藏
    },
  },
  // 404
  {
    // 404
    path: '/404',
    component: () => import('@/views/404/index.vue'),
    name: '404',
    meta: {
      title: '404', // 菜单标题
      hidden: true, // 代表是否隐藏
      // icon: 'Promotion',
    },
  },

  // 数据库管理
  // {
  //   path: '/database',
  //   component: () => import('@/layout/index.vue'),
  //   name: 'Database',
  //   meta: {
  //     title: '数据库', // 菜单标题
  //     hidden: false, // 代表是否隐藏
  //     // icon: 'Box',
  //   },
  //   redirect: '/database/manage',
  //   children: [
  //     {
  //       path: '/database/manage',
  //       component: () => import('@/views/database/index.vue'),
  //       name: 'Database',
  //       meta: {
  //         title: '数据库管理', // 菜单标题
  //         hidden: false, // 代表是否隐藏
  //         icon: 'Coin',
  //       },
  //     },
  //   ],
  // },
  // // 库存管理
  // {
  //   path: '/inventory',
  //   component: () => import('@/layout/index.vue'),
  //   name: 'Inventory',
  //   meta: {
  //     title: '仓库管理', // 菜单标题
  //     hidden: false, // 代表是否隐藏
  //     // icon: 'Box',
  //   },
  //   redirect: '/inventory/manage',
  //   children: [
  //     {
  //       path: '/inventory/manage',
  //       component: () => import('@/views/inventory/index.vue'),
  //       name: 'Inventory',
  //       meta: {
  //         title: '库存管理', // 菜单标题
  //         hidden: false, // 代表是否隐藏
  //         icon: 'Box',
  //       },
  //     },
  //     {
  //       path: '/inventory/statistics',
  //       component: () => import('@/views/inventory/statistics/index.vue'),
  //       name: 'InventoryStatistics',
  //       meta: {
  //         title: '库存统计', // 菜单标题
  //         hidden: false, // 代表是否隐藏
  //         icon: 'Histogram',
  //       },
  //     },
  //   ],
  // },
  // // 优惠管理
  // {
  //   path: '/discount',
  //   component: () => import('@/layout/index.vue'),
  //   name: 'Discount',
  //   meta: {
  //     title: '优惠管理', // 菜单标题
  //     hidden: false, // 代表是否隐藏
  //     // icon: 'Box',
  //   },
  //   children: [
  //     {
  //       path: '/discount/manage',
  //       component: () => import('@/views/discount/index.vue'),
  //       name: 'DiscountManage',
  //       meta: {
  //         title: '优惠管理', // 菜单标题
  //         hidden: false, // 代表是否隐藏
  //         icon: 'SoldOut',
  //       },
  //     },
  //   ],
  // },
  // // test
  // {
  //   path: '/test',
  //   component: () => import('@/views/test.vue'),
  //   meta: {
  //     title: 'test', // 菜单标题
  //     hidden: false, // 代表是否隐藏
  //     icon: 'test',
  //   },
  // },
  // {
  //   path: '/acl',
  //   component: () => import('@/layout/index.vue'),
  //   name: 'Acl',
  //   meta: {
  //     title: '权限管理', // 菜单标题
  //     hidden: false, // 代表是否隐藏
  //     icon: 'Lock',
  //   },
  //   redirect: '/acl/user',
  //   children: [
  //     {
  //       path: '/acl/user',
  //       name: 'User',
  //       component: () => import('@/views/acl/user/index.vue'),
  //       meta: {
  //         title: '用户管理', // 菜单标题
  //         hidden: false, // 代表是否隐藏
  //         icon: 'User',
  //       },
  //     },
  //     {
  //       path: '/acl/role',
  //       name: 'Role',
  //       component: () => import('@/views/acl/role/index.vue'),
  //       meta: {
  //         title: '角色管理', // 菜单标题
  //         hidden: false, // 代表是否隐藏
  //         icon: 'UserFilled',
  //       },
  //     },
  //     {
  //       path: '/acl/permission',
  //       name: 'Permission',
  //       component: () => import('@/views/acl/permission/index.vue'),
  //       meta: {
  //         title: '菜单管理', // 菜单标题
  //         hidden: false, // 代表是否隐藏
  //         icon: 'Platform',
  //       },
  //     },
  //   ],
  // },
  // {
  //   path: '/goods',
  //   component: () => import('@/layout/index.vue'),
  //   name: '',
  //   meta: {
  //     title: '', // 菜单标题
  //     hidden: false, // 代表是否隐藏
  //     // icon: '',
  //   },
  //   children: [
  //     {
  //       path: '/goods/manage',
  //       component: () => import('@/views/goods/index.vue'),
  //       meta: {
  //         title: '商品管理', // 菜单标题
  //         hidden: false, // 代表是否隐藏
  //         icon: 'Goods',
  //       },
  //     },
  //   ],
  // },
]

// 异步路由：
export const asyncRoute = [
  // 权限管理
  {
    path: '/acl',
    component: () => import('@/layout/index.vue'),
    name: 'Acl',
    meta: {
      title: '权限管理', // 菜单标题
      hidden: false, // 代表是否隐藏
      icon: 'Lock',
    },
    redirect: '/acl/user',
    children: [
      {
        path: '/acl/user',
        name: 'User',
        component: () => import('@/views/acl/user/index.vue'),
        meta: {
          title: '用户管理', // 菜单标题
          hidden: false, // 代表是否隐藏
          icon: 'User',
        },
      },
      {
        path: '/acl/role',
        name: 'Role',
        component: () => import('@/views/acl/role/index.vue'),
        meta: {
          title: '角色管理', // 菜单标题
          hidden: false, // 代表是否隐藏
          icon: 'UserFilled',
        },
      },
      {
        path: '/acl/permission',
        name: 'Permission',
        component: () => import('@/views/acl/permission/index.vue'),
        meta: {
          title: '菜单管理', // 菜单标题
          hidden: false, // 代表是否隐藏
          icon: 'Platform',
        },
      },
    ],
  },
  // 商品管理
  {
    path: '/goods',
    component: () => import('@/layout/index.vue'),
    name: 'Goods',
    meta: {
      title: '', // 菜单标题
      hidden: false, // 代表是否隐藏
      // icon: '',
    },
    redirect: '/goods/manage',
    children: [
      {
        path: '/goods/manage',
        component: () => import('@/views/goods/index.vue'),
        name: 'Goods',
        meta: {
          title: '商品管理', // 菜单标题
          hidden: false, // 代表是否隐藏
          icon: 'Goods',
        },
      },
    ],
  },
  // 库存管理
  {
    path: '/inventory',
    component: () => import('@/layout/index.vue'),
    name: 'Inventory',
    meta: {
      title: '库存管理', // 菜单标题
      hidden: false, // 代表是否隐藏
      icon: 'Box',
    },
    redirect: '/inventory/manage',
    children: [
      {
        path: '/inventory/manage',
        component: () => import('@/views/inventory/index.vue'),
        name: 'Inventory',
        meta: {
          title: '库存管理', // 菜单标题
          hidden: false, // 代表是否隐藏
          icon: 'Box',
        },
      },
      {
        path: '/inventory/statistics',
        component: () => import('@/views/inventory/statistics/index.vue'),
        name: 'InventoryStatistics',
        meta: {
          title: '库存统计', // 菜单标题
          hidden: false, // 代表是否隐藏
          icon: 'Histogram',
        },
      },
    ],
  },
  // 销售管理
  {
    path: '/sell',
    component: () => import('@/layout/index.vue'),
    name: 'Sell',
    meta: {
      title: '销售管理', // 菜单标题
      hidden: false, // 代表是否隐藏
      icon: 'DataAnalysis',
    },
    redirect: '/sell/receipt',
    children: [
      {
        path: '/sell/receipt',
        name: 'Receipt',
        component: () => import('@/views/sell/receipt/index.vue'),
        meta: {
          title: '销售记录', // 菜单标题
          hidden: false, // 代表是否隐藏
          icon: 'Tickets',
        },
      },
      {
        path: '/sell/detail',
        name: 'Detail',
        component: () => import('@/views/sell/detail/index.vue'),
        meta: {
          title: '销售统计', // 菜单标题
          hidden: false, // 代表是否隐藏
          icon: 'DataLine',
        },
      },
    ],
  },
  // 会员管理
  {
    path: '/customer',
    component: () => import('@/layout/index.vue'),
    name: 'Customer',
    meta: {
      title: '会员管理', // 菜单标题
      hidden: false, // 代表是否隐藏
      icon: 'Avatar',
    },
    children: [
      {
        path: '/customer/manage',
        component: () => import('@/views/customer/index.vue'),
        name: 'CustomerManage',
        meta: {
          title: '会员信息管理', // 菜单标题
          hidden: false, // 代表是否隐藏
          icon: 'Document',
        },
      },
      {
        path: '/customer/level',
        component: () => import('@/views/discount/index.vue'),
        name: 'CustomerLevelManage',
        meta: {
          title: '会员等级管理', // 菜单标题
          hidden: false, // 代表是否隐藏
          icon: 'GoldMedal',
        },
      },
    ],
  },
  // 会员中心
  {
    path: '/member',
    component: () => import('@/layout/index.vue'),
    name: 'Member',
    meta: {
      title: '会员中心', // 菜单标题
      hidden: false, // 代表是否隐藏
      icon: 'Avatar',
    },
    redirect: '/member/center',
    children: [
      {
        path: '/member/receipt',
        component: () => import('@/views/member/memberReceipt/index.vue'),
        name: 'memberReceipt',
        meta: {
          title: '消费记录', // 菜单标题
          hidden: false, // 代表是否隐藏
          icon: 'List', // 图标
        },
      },
      {
        path: '/member/info',
        component: () => import('@/views/member/memberInfo/index.vue'),
        name: 'memberInfo',
        meta: {
          title: '会员信息', // 菜单标题
          hidden: false, // 代表是否隐藏
          icon: 'Document', // 图标
        },
      },
    ],
  },
  // 数据库管理
  {
    path: '/database',
    component: () => import('@/layout/index.vue'),
    name: 'Database',
    meta: {
      title: '数据库', // 菜单标题
      hidden: false, // 代表是否隐藏
      // icon: 'Box',
    },
    redirect: '/database/manage',
    children: [
      {
        path: '/database/manage',
        component: () => import('@/views/database/index.vue'),
        name: 'Database',
        meta: {
          title: '数据库管理', // 菜单标题
          hidden: false, // 代表是否隐藏
          icon: 'Coin',
        },
      },
    ],
  },
  // 检测
  {
    path: '/screen',
    component: () => import('@/views/screen/index.vue'),
    name: 'Stock-in',
    meta: {
      name: 'Stock-in',
      title: '入库平台', // 菜单标题
      hidden: false, // 代表是否隐藏
      icon: 'Monitor',
    },
  },
  // 售货平台
  {
    path: '/sale',
    component: () => import('@/views/sale/index.vue'),
    name: 'Sale',
    meta: {
      name: 'Sale',
      title: '售货平台', // 菜单标题
      hidden: false, // 代表是否隐藏
      icon: 'Wallet',
    },
  },
  // 任意路由
  // {
  //   // 404
  //   path: '/:pathMatch(.*)*',
  //   redirect: '/404',
  //   name: 'Any',
  //   meta: {
  //     title: '任意路由', // 菜单标题
  //     hidden: true, // 代表是否隐藏
  //     // icon: 'Promotion',
  //   },
  // },
]

//任意路由
export const anyRoute = {
  //任意路由
  path: '/:pathMatch(.*)*',
  redirect: '/404',
  name: 'Any',
  meta: {
    title: '任意路由',
    hidden: true,
    // icon: 'DataLine',
  },
}

// // 任意路由
// export const anyRoute = [
//   {
//     // 404
//     path: '/:pathMatch(.*)*',
//     redirect: '/404',
//     name: 'Any',
//     meta: {
//       title: '任意路由', // 菜单标题
//       hidden: true, // 代表是否隐藏
//       // icon: 'Promotion',
//     },
//   },
// ]
