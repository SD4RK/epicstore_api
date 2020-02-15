# -*- coding: utf-8 -*-

"""
MIT License

Copyright (c) 2020 SD4RK

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""


CATALOG_QUERY = "\n            query catalogQuery(\n                $category:String,\n                $count:Int,\n                $country:String!,\n                $keywords: String,\n                $locale:String,\n                $namespace:String!,\n                $sortBy:String,\n                $sortDir:String,\n                $start:Int,\n                $tag:String\n            ) {\n                Catalog {\n                    catalogOffers(\n                        namespace: $namespace,\n                        locale: $locale,\n                        params: {\n                            count: $count,\n                            country: $country,\n                            category: $category,\n                            keywords: $keywords,\n                            sortBy: $sortBy,\n                            sortDir: $sortDir,\n                            start: $start,\n                            tag: $tag\n                        }\n                    ) {\n                        elements {\n                            isFeatured\n                            collectionOfferIds\n                            \n          title\n          id\n          namespace\n          description\n          keyImages {\n            type\n            url\n          }\n          seller {\n              id\n              name\n          }\n          productSlug\n          urlSlug\n          items {\n            id\n            namespace\n          }\n          customAttributes {\n            key\n            value\n          }\n          categories {\n            path\n          }\n          price(country: $country) {\n            totalPrice {\n              discountPrice\n              originalPrice\n              voucherDiscount\n              discount\n              fmtPrice(locale: $locale) {\n                originalPrice\n                discountPrice\n                intermediatePrice\n              }\n            }\n            lineOffers {\n              appliedRules {\n                id\n                endDate\n              }\n            }\n          }\n          linkedOfferId\n          linkedOffer {\n            effectiveDate\n            customAttributes {\n              key\n              value\n            }\n          }\n        \n                        }\n                        paging {\n                            count,\n                            total\n                        }\n                    }\n                }\n            }\n        "
PROMOTIONS_QUERY = "\n          query promotionsQuery($namespace: String!, $country: String!, $locale: String!) {\n            Catalog {\n              catalogOffers(namespace: $namespace, locale: $locale, params: {category: \"freegames\", country: $country, sortBy: \"effectiveDate\", sortDir: \"asc\"}) {\n                elements {\n                  title\n                  description\n                  id\n                  namespace\n                  categories {\n                    path\n                  }\n                  linkedOfferNs\n                  linkedOfferId\n                  keyImages {\n                    type\n                    url\n                  }\n                  productSlug\n                  promotions {\n                    promotionalOffers {\n                      promotionalOffers {\n                        startDate\n                        endDate\n                        discountSetting {\n                          discountType\n                          discountPercentage\n                        }\n                      }\n                    }\n                    upcomingPromotionalOffers {\n                      promotionalOffers {\n                        startDate\n                        endDate\n                        discountSetting {\n                          discountType\n                          discountPercentage\n                        }\n                      }\n                    }\n                  }\n                }\n              }\n            }\n          }\n        "
CATALOG_TAGS_QUERY = "\n            query catalogTags($namespace: String!)\n            {\n                Catalog {\n                    tags (\n                        namespace: $namespace,\n                        start: 0,\n                        count: 999\n                    ) {\n                        elements {\n                            aliases,\n                            id,\n                            name,\n                            referenceCount,\n                            status\n                        }\n                    }\n                }\n            }\n            "
FEED_QUERY = "\n            query feedQuery($locale: String!, $countryCode: String, $offset: Int, $postsPerPage: Int, $category: String) {\n                TransientStream {\n                    myTransientFeed(countryCode: $countryCode, locale: $locale) {\n                        id\n                        activity {\n                            # TODO Comment in to enable welcome post when requirements are finalized\n                            # ...on SimpleActivity {\n                            #     type\n                            #     created_at\n                            # }\n                            ...on LinkAccountActivity {\n                                type\n                                created_at\n                                platforms\n                            }\n                            ...on SuggestedFriendsActivity {\n                                type\n                                created_at\n                                platform\n                                suggestions {\n                                    epicId\n                                    epicDisplayName\n                                    platformFullName\n                                    platformAvatar\n                                }\n                            }\n                            ...on IncomingInvitesActivity {\n                                type\n                                created_at\n                                invites {\n                                    epicId\n                                    epicDisplayName\n                                }\n                            }\n                            ...on RecentPlayersActivity {\n                                type\n                                created_at\n                                players {\n                                    epicId\n                                    epicDisplayName\n                                    playedGameName\n                                }\n                            }\n                        }\n                    }\n                }\n                Blog {\n                    dieselBlogPosts: getPosts(locale: $locale, offset: $offset, postsPerPage: $postsPerPage, category: $category) {\n                        blogList {\n                            _id\n                            author\n                            category\n                            content\n                            urlPattern\n                            slug\n                            sticky\n                            title\n                            date\n                            image\n                            shareImage\n                            trendingImage\n                            url\n                            featured\n                            link\n                            externalLink\n                        }\n                    }\n                }\n            }"
PREREQUISITES_QUERY = "\n    query fetchPrerequisites($offerParams: [OfferParams]) {\n        Launcher{\n            prerequisites(offerParams:$offerParams) {\n                namespace,\n                offerId,\n                missingPrerequisiteItems\n                satisfiesPrerequisites\n            }\n        }\n    }\n"
OFFERS_QUERY = "\n        query catalogQuery(\n            $productNamespace:String!,\n            $offerId:String!,\n            $locale:String,\n            $country:String!,\n            $lineOffers: [LineOfferReq]!) {\n                Catalog {\n                    catalogOffer(namespace: $productNamespace,\n                        id: $offerId,\n                        locale: $locale) {\n                            namespace\n                            effectiveDate\n                            id\n                            customAttributes {\n                                key\n                                value\n                            }\n                            items {\n                                id\n                                status\n                                customAttributes {\n                                    key\n                                    value\n                                }\n                            }\n                    }\n                }\n                PriceEngine {\n                    price(country: $country, lineOffers: $lineOffers) {\n                        totalPrice {\n                            discountPrice\n                            originalPrice\n                            voucherDiscount\n                            discount\n                            currencyCode\n                            currencyInfo {\n                                decimals\n                            }\n                            fmtPrice(locale: $locale) {\n                                originalPrice\n                                discountPrice\n                                intermediatePrice\n                            }\n                        }\n                        lineOffers {\n                            appliedRules {\n                                endDate\n                                discountSetting {\n                                    discountType\n                                }\n                            }\n                        }\n                    }\n                }\n            }\n        "
# XXX: This code violates PEP 8, line > 79 chars
