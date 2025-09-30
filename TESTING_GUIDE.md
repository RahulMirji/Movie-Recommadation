# 🧪 Quick Testing Guide - XML Export Feature

## ✅ **Step-by-Step Testing Instructions**

### **Test 1: Verify New Moods Are Visible**

1. Open browser: http://127.0.0.1:5000
2. Click on "Your Current Mood" dropdown
3. Verify you see all 9 options:
   - ✨ Select your mood...
   - 😊 Happy - Fun & Uplifting
   - 😢 Sad - Emotional & Moving
   - 😡 Angry - Intense & Thrilling
   - 💕 Romantic - Love & Romance
   - 🌟 Inspired - Motivational & Uplifting
   - 🏞️ Adventurous - Exciting & Bold
   - 🔍 Curious - Mystery & Suspense ← NEW
   - 😂 Funny - Comedy & Lighthearted ← NEW
   - 🌌 Dreamy - Fantasy & Magical ← NEW

✅ **Expected:** All 9 moods visible with correct emojis

---

### **Test 2: Generate Recommendations with New Moods**

#### Test 2A: Curious Mood
1. Select "🔍 Curious - Mystery & Suspense"
2. Select "Hindi" language
3. Click "Find My Movies"
4. Verify you get 15 mystery/thriller movies
5. Expected movies: Kahaani, Drishyam, Andhadhun, Talvar, etc.

✅ **Expected:** 15 relevant mystery/suspense movies displayed

#### Test 2B: Funny Mood
1. Select "😂 Funny - Comedy & Lighthearted"
2. Select "English" language
3. Click "Find My Movies"
4. Verify you get 15 comedy movies
5. Expected movies: The Hangover, Superbad, Deadpool, etc.

✅ **Expected:** 15 comedy movies displayed

#### Test 2C: Dreamy Mood
1. Select "🌌 Dreamy - Fantasy & Magical"
2. Select "Malayalam" language
3. Click "Find My Movies"
4. Verify you get 15 romantic/fantasy movies
5. Expected movies: Premam, Bangalore Days, Charlie, etc.

✅ **Expected:** 15 dreamy/romantic movies displayed

---

### **Test 3: XML Export Button - The Main Fix**

#### Step 1: Generate Recommendations
1. Go to: http://127.0.0.1:5000
2. Select any mood (e.g., "Curious")
3. Select any language (e.g., "Hindi")
4. Click "Find My Movies"
5. Wait for results to load

#### Step 2: Test XML Export
1. Look for buttons below the movie table
2. You should see three buttons:
   - 🔍 Find More Movies
   - 🖨️ Save Results
   - 📤 **Export to XML** ← Click this one
   - 🔗 Share (dropdown)

3. Click "Export to XML" button

#### Step 3: Verify Download
**What Should Happen:**
- ✅ Toast notification: "Downloading XML file..."
- ✅ Browser download starts automatically
- ✅ File downloads with name like: `movie_recommendations_Curious_Hindi_20250930_213045.xml`
- ✅ No errors in browser console

**If Download Fails:**
- Check browser console (F12) for errors
- Check terminal for Python errors
- Verify exports/ folder exists

#### Step 4: Verify XML File
1. Open the downloaded XML file in text editor or browser
2. Verify structure:

```xml
<?xml version='1.0' encoding='utf-8'?>
<MovieRecommendations>
  <Metadata>
    <Mood>Curious</Mood>
    <Language>Hindi</Language>
    <GeneratedOn>2025-09-30 21:30:45</GeneratedOn>
    <TotalMovies>15</TotalMovies>
  </Metadata>
  <Movies>
    <Movie id="1">
      <Title>Kahaani</Title>
      <Rating>8.1</Rating>
      <Summary>A pregnant woman's search...</Summary>
      <Popularity>74,523 votes</Popularity>
    </Movie>
    <!-- More movies... -->
  </Movies>
</MovieRecommendations>
```

✅ **Expected:** 
- Valid XML structure
- Correct mood and language
- 15 movie entries
- All fields populated

---

### **Test 4: Check Exports Folder**

1. Navigate to: `d:\Movie-Recommadation\exports\`
2. Verify XML file is saved there
3. Each export creates a new file (not overwriting)
4. Filename includes timestamp

✅ **Expected:** XML files accumulate in exports/ folder

---

### **Test 5: Error Handling**

#### Test 5A: Multiple Rapid Clicks
1. Generate recommendations
2. Click "Export to XML" multiple times quickly
3. Verify: Multiple files download without errors

✅ **Expected:** Each click generates a new file

#### Test 5B: Browser Console
1. Open browser console (F12)
2. Click "Export to XML"
3. Check for JavaScript errors

✅ **Expected:** No errors in console

---

### **Test 6: All Mood-Language Combinations**

Test a few random combinations to ensure database completeness:

1. **Happy + Kannada** → Should show Kirik Party, KGF, etc.
2. **Sad + Tamil** → Should show 96, Kaaka Muttai, etc.
3. **Angry + Telugu** → Should show Rangasthalam, Pushpa, etc.
4. **Romantic + English** → Should show Titanic, La La Land, etc.
5. **Inspired + Malayalam** → Should show Virus, Minnal Murali, etc.
6. **Adventurous + Hindi** → Should show Pathaan, War, etc.
7. **Curious + Kannada** → Should show Kavaludaari, U Turn, etc.
8. **Funny + Tamil** → Should show Soodhu Kavvum, Comali, etc.
9. **Dreamy + Telugu** → Should show Ye Maaya Chesave, Premam, etc.

✅ **Expected:** All combinations return 15 relevant movies

---

## 🐛 **Common Issues & Solutions**

### Issue 1: "Export to XML" button does nothing

**Possible Causes:**
- JavaScript error
- Function not in global scope
- Browser blocking download

**Solutions:**
- Open console (F12) and check for errors
- Clear browser cache (Ctrl + Shift + R)
- Try different browser
- Check if pop-ups are blocked

---

### Issue 2: XML file downloads but is empty or corrupted

**Possible Causes:**
- Server error
- Missing data
- Encoding issue

**Solutions:**
- Check terminal for Python errors
- Verify OMDB_API_KEY in .env file
- Check exports/ folder permissions
- Restart Flask server

---

### Issue 3: Toast notification doesn't show

**Possible Causes:**
- window.movieUI not initialized
- Toast container missing

**Solutions:**
- Alert will show as fallback
- File should still download
- Check if base.html loaded correctly

---

### Issue 4: "Failed to export XML" error

**Possible Causes:**
- Server crash
- Invalid mood/language
- File system permissions

**Solutions:**
- Check terminal for error details
- Verify exports/ folder exists
- Check disk space
- Restart server

---

## 📊 **Test Results Checklist**

Use this checklist to verify everything works:

- [ ] All 9 moods visible in dropdown
- [ ] All 6 languages visible in dropdown
- [ ] Curious mood shows mystery movies
- [ ] Funny mood shows comedy movies
- [ ] Dreamy mood shows romantic movies
- [ ] "Export to XML" button is visible
- [ ] Clicking button shows toast notification
- [ ] XML file downloads automatically
- [ ] Downloaded file is valid XML
- [ ] File contains correct metadata
- [ ] File contains 15 movies
- [ ] File saved in exports/ folder
- [ ] Multiple exports work correctly
- [ ] No console errors
- [ ] No terminal errors
- [ ] All mood-language combos work

---

## 🎯 **Quick Test Commands**

### Test Server Status:
```powershell
# Check if server is running
curl http://127.0.0.1:5000/health
```

**Expected Response:**
```json
{"service":"movie-recommender","status":"healthy"}
```

### Test API Endpoint:
```powershell
# Test recommendations API
curl -X POST http://127.0.0.1:5000/api/recommendations -H "Content-Type: application/json" -d "{\"mood\":\"Curious\",\"language\":\"Hindi\"}"
```

**Expected:** JSON array with 15 movie objects

---

## 🎉 **Success Criteria**

Your system is working correctly if:

✅ All 9 moods are selectable  
✅ All mood-language combinations return movies  
✅ XML export button downloads file  
✅ Downloaded XML is valid and complete  
✅ No errors in console or terminal  
✅ Toast notifications appear  
✅ Files save to exports/ folder  

---

## 📞 **Need Help?**

If XML export still doesn't work:

1. **Check Terminal Output:**
   - Look for Python errors
   - Check OMDb API errors
   - Verify Flask is running

2. **Check Browser Console:**
   - Press F12
   - Look in Console tab
   - Check Network tab for failed requests

3. **Manual Test:**
   - Try opening: http://127.0.0.1:5000/export/xml directly
   - Should show error (405 Method Not Allowed) - this is normal

4. **Verify Files:**
   - Check if exports/ folder exists
   - Check folder permissions
   - Try creating file manually in exports/

---

**Happy Testing! 🚀**

If all tests pass, your Movie Recommendation System with XML export is fully functional! 🎬✨
