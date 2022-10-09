// @ts-check
// Note: type annotations allow type checking and IDEs autocompletion

const lightCodeTheme = require('prism-react-renderer/themes/github');
const darkCodeTheme = require('prism-react-renderer/themes/dracula');

/** @type {import('@docusaurus/types').Config} */
const config = {
  title: 'Netdata Blog',
  tagline: 'Home of the Netdata blog',
  url: 'https://reliable-dolphin-966b1b.netlify.app',
  baseUrl: '/',
  onBrokenLinks: 'throw',
  onBrokenMarkdownLinks: 'warn',
  favicon: 'img/favicon.ico',

  // Even if you don't use internalization, you can use this field to set useful
  // metadata like html lang. For example, if your site is Chinese, you may want
  // to replace "en" with "zh-Hans".
  i18n: {
    defaultLocale: 'en',
    locales: ['en'],
  },

  themes: [
    [
      require.resolve("@easyops-cn/docusaurus-search-local"),
      {
        hashed: true,
        indexDocs: false,
        indexBlog: true,
        blogRouteBasePath: "./blog"
      },
    ],
  ],

  presets: [
    [
      'classic',
      /** @type {import('@docusaurus/preset-classic').Options} */
      ({
        docs: false,
        blog: {
          routeBasePath: '/', 
          showReadingTime: true,
          blogSidebarTitle: 'All posts',
          blogSidebarCount: 'ALL',
          feedOptions: {
            type: 'all',
            copyright: `Copyright © ${new Date().getFullYear()} Netdata`,
          },
        },
        theme: {
          customCss: require.resolve('./src/css/custom.css'),
        },
      }),
    ],
  ],

  themeConfig:
    /** @type {import('@docusaurus/preset-classic').ThemeConfig} */
    ({
      navbar: {
        title: 'Blog',
        logo: {
          alt: 'Netdata',
          src: 'img/logo.svg',
        },
        items: [
            {
                href: 'https://www.netdata.cloud/',
                label: 'Website',
                position: 'left',
              },
              {
                href: 'https://learn.netdata.cloud/',
                label: 'Learn',
                position: 'left',
              },
              {
                href: 'https://app.netdata.cloud/',
                label: 'Sign In',
                position: 'right',
              },
        ],
      },
      footer: {
        style: 'dark',
        links: [
            {
                title: 'Products',
                items: [
                    {
                        label: 'Agent',
                        to: 'https://netdata.cloud/agent',
                    },
                    {
                        label: 'Cloud',
                        to: 'https://netdata.cloud/cloud',
                    },
                    {
                        label: 'Integrations',
                        to: 'https://www.netdata.cloud/integrations/',
                    },
                    {
                        label: 'Status',
                        to: 'https://status.netdata.cloud',
                    },
                ],
            },
            {
                title: 'Resources',
                items: [
                    {
                        label: 'Learn',
                        to: '/',
                    },
                    {
                        label: 'Blog',
                        to: 'https://netdata.cloud/blog',
                    },
                    {
                        label: 'GitHub',
                        to: 'https://github.com/netdata/netdata',
                    },
                ],
            },
            {
                title: 'Community',
                items: [
                    {
                        label: 'Overview',
                        to: 'https://www.netdata.cloud/community-overview/',
                    },
                    {
                        label: 'Forums',
                        to: 'https://community.netdata.cloud/',
                    },
                ],
            },
            {
                title: 'Company',
                items: [
                    {
                        label: 'About',
                        to: 'https://netdata.cloud',
                    },
                    {
                        label: 'News',
                        to: 'https://www.netdata.cloud/news/',
                    },
                    {
                        label: 'Careers',
                        to: 'https://careers.netdata.cloud/',
                    },
                ],
            },
        ],
        copyright: `Copyright © ${new Date().getFullYear()} Netdata, Inc.`,
    },
      prism: {
        theme: lightCodeTheme,
        darkTheme: darkCodeTheme,
      },
    }),
};

module.exports = config;
//module.exports = [
//    config,
//    {
//    url: 'https://main--reliable-dolphin-966b1b.netlify.app',
//    baseUrl: '/',
//  }];