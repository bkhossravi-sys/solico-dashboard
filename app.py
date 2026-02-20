<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        @import url('https://v1.fontapi.ir/css/Vazir');
        body { font-family: 'Vazir', sans-serif; background-color: #f4f7f9; }
        .radar-placeholder {
            background: radial-gradient(circle, #2dd4bf 10%, transparent 10%),
                        radial-gradient(circle, transparent 20%, #134e4a 20%, #134e4a 21%, transparent 21%);
            background-size: 20px 20px, 100% 100%;
        }
    </style>
</head>
<body class="pb-20">

    <header class="bg-white border-b p-4 flex justify-between items-center sticky top-0 z-10">
        <button class="text-gray-500">✕</button>
        <div class="text-center">
            <h1 class="text-sm font-bold text-gray-800">داشبورد فروش</h1>
            <p class="text-[10px] text-gray-400 uppercase tracking-widest">Market Analysis Report</p>
        </div>
        <button class="text-yellow-500">🔍</button>
    </header>

    <main class="p-4 space-y-4">
        
        <div class="bg-white p-4 rounded-lg shadow-sm border border-gray-100 relative overflow-hidden">
            <h3 class="text-xs font-semibold text-gray-500 mb-2">سهم بازار کل (هدف)</h3>
            <div class="flex flex-col items-center justify-center py-4">
                <div class="relative w-40 h-20 overflow-hidden">
                    <div class="absolute top-0 left-0 w-40 h-40 border-[16px] border-gray-100 rounded-full"></div>
                    <div class="absolute top-0 left-0 w-40 h-40 border-[16px] border-teal-500 rounded-full border-b-transparent border-r-transparent rotate-[45deg]"></div>
                </div>
                <span class="text-2xl font-black text-gray-700 mt-[-20px]">۷۴۵.۸۵</span>
                <div class="flex justify-between w-full text-[10px] text-gray-400 mt-2">
                    <span>۰.۰</span>
                    <span>۱,۴۹۱.۷</span>
                </div>
            </div>
        </div>

        <div class="bg-white p-4 rounded-lg shadow-sm border border-gray-100">
            <h3 class="text-xs font-semibold text-gray-500 mb-4">رتبه‌بندی نفوذ برند (محصولات غذایی)</h3>
            <div class="space-y-3">
                <div class="flex items-center gap-2">
                    <span class="text-[10px] w-12 text-gray-400 italic">کاله</span>
                    <div class="flex-1 bg-gray-100 h-6 rounded relative overflow-hidden">
                        <div class="bg-blue-500 h-full w-[90%] transition-all duration-1000"></div>
                        <span class="absolute inset-y-0 right-2 flex items-center text-[10px] text-white font-bold">۱۵۵ میلیون</span>
                    </div>
                </div>
                <div class="flex items-center gap-2">
                    <span class="text-[10px] w-12 text-gray-400 italic">بیژن</span>
                    <div class="flex-1 bg-gray-100 h-6 rounded relative overflow-hidden">
                        <div class="bg-blue-400 h-full w-[70%]"></div>
                        <span class="absolute inset-y-0 right-2 flex items-center text-[10px] text-white font-bold">۱۲۳ میلیون</span>
                    </div>
                </div>
                <div class="flex items-center gap-2">
                    <span class="text-[10px] w-12 text-gray-400 italic">مهرام</span>
                    <div class="flex-1 bg-gray-100 h-6 rounded relative overflow-hidden">
                        <div class="bg-blue-300 h-full w-[45%]"></div>
                        <span class="absolute inset-y-0 right-2 flex items-center text-[10px] text-white font-bold">۶۷ میلیون</span>
                    </div>
                </div>
            </div>
        </div>

        <div class="grid grid-cols-2 gap-4">
            <div class="bg-white p-3 rounded-lg border border-gray-100 text-center">
                <p class="text-[10px] text-gray-400">رشد سالانه</p>
                <p class="text-lg font-bold text-green-500">+۱۲.۴٪</p>
            </div>
            <div class="bg-white p-3 rounded-lg border border-gray-100 text-center">
                <p class="text-[10px] text-gray-400">تعداد محصول</p>
                <p class="text-lg font-bold text-gray-700">۴۳۸</p>
            </div>
        </div>

    </main>

    <nav class="fixed bottom-0 left-0 right-0 bg-[#333] text-white h-16 flex justify-around items-center">
        <div class="flex flex-col items-center opacity-50">
            <span class="text-xs">⭐</span>
            <span class="text-[10px]">علاقه‌مندی</span>
        </div>
        <div class="flex flex-col items-center border-t-2 border-white pt-1">
            <span class="text-xs">📊</span>
            <span class="text-[10px]">داشبورد</span>
        </div>
        <div class="flex flex-col items-center opacity-50">
            <span class="text-xs">🔔</span>
            <span class="text-[10px]">هشدارها</span>
        </div>
        <div class="flex flex-col items-center opacity-50">
            <span class="text-xs">⚙️</span>
            <span class="text-[10px]">تنظیمات</span>
        </div>
    </nav>

</body>
</html>
